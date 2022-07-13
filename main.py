import time

initialtime = time.time()

def importAirlines(filename, commentprefix):
    airlines = {}
    file = open(filename)
    allairlines = file.readlines()
    file.close()
    for i in range(len(allairlines)):
        if allairlines[i][0:2] != commentprefix:
            ICAO_code = allairlines[i][0:3]
            game_code = allairlines[i][5:7]
            airlines[game_code] = ICAO_code
    return airlines

def importGATraffic(filename, commentprefix, arrivalairportcode):
    GA_departures = []
    GA_arrivals = []
    file = open(filename)
    GA_planes = file.readlines()
    file.close()
    for i in range(0, len(GA_planes)):
        if GA_planes[i][1:4] == arrivalairportcode:
            GA_departures.append(GA_planes[i])
        elif GA_planes[i][0:2] != commentprefix:
            GA_arrivals.append(GA_planes[i])
    GA_departure_count = len(GA_departures)
    GA_arrival_count = len(GA_arrivals)
    return GA_departures, GA_arrivals, GA_departure_count, GA_arrival_count

def importCommercialTraffic(filename, commentprefix, arrivalairportcode):
    departures = []
    arrivals = []
    file = open(filename)
    commercial_planes = file.readlines()
    file.close()
    for i in range(0, len(commercial_planes)):
        if commercial_planes[i][0:3] == arrivalairportcode:
            departures.append(commercial_planes[i].split(","))
        elif commercial_planes[i][0:2] != commentprefix:
            arrivals.append(commercial_planes[i].split(","))
    departure_count = len(departures)
    arrival_count = len(arrivals)
    return departures, arrivals, departure_count, arrival_count

def importGameLog(filename):
    file = open(filename)
    logfile_contents = file.readlines()
    file.close()
    logged_instructions = []
    for i in range(0, len(logfile_contents)):
        if logfile_contents[i][0:8] == "COMMAND:":
            logged_instructions.append(logfile_contents[i][9:].split(" "))
    return logged_instructions

def calculateHandledAircraft(logged_instructions, GA_departures, GA_arrivals, departures, arrivals, airlines, terminal_synonyms, banned_runways):
    unhandled = []
    # GA processing needs review! Currently can't test GA as I don't have any GA schedules
    GA_departure_count = 0
    for i in range(0, len(GA_departures)):
        target_callsign = (airlines[GA_departures[i][3].replace(" ", "")] + GA_departures[i][4]).replace(" ", "")

    GA_arrival_count = 0
    for i in range(0, len(GA_arrivals)):
        target_callsign = (airlines[GA_arrivals[i][3].replace(" ", "")] + GA_arrivals[i][4]).replace(" ", "")
    
    departure_count = 0
    for i in range(0, len(departures)):
        target_callsign = (airlines[departures[i][3].replace(" ", "")] + departures[i][4]).replace(" ", "")
        # for a departure, check for a pushback, taxi to RWY, takeoff,
        pushback = False
        taxi = False
        takeoff = False
        handoff = False
        for j in range(0, len(logged_instructions)):
            # filtering all instructions applicable to this callsign
            if target_callsign in logged_instructions[j][0]:
                # check if current instruction is a VALID takeoff clearance
                if len(logged_instructions[j]) >= 6 and ("TAKEOFF" in logged_instructions[j][5] or "TAKEOFF" in logged_instructions[j][-1]) and logged_instructions[j][2] not in banned_runways:
                    takeoff = True
                    # handles handoff check for all handoffs at the end of messages
                    if "DEPARTURE" in logged_instructions[j][-1]:
                        handoff = True
                # check if current instruction is a pushback clearance
                elif len(logged_instructions[j]) >= 6 and "PUSHBACK" in logged_instructions[j][1]:
                    pushback = True
                # check if current instruction is a taxi clearance
                elif len(logged_instructions[j]) >= 4 and "RUNWAY" in logged_instructions[j][1]:
                    taxi = True
                # check if current instruction is departure handoff
                elif len(logged_instructions[j]) == 3 and "DEPARTURE" in logged_instructions[j][2]:
                    handoff = True
        
        if pushback and taxi and takeoff and handoff:
            departure_count += 1
        else:
            unhandled.append({"Callsign": target_callsign, "Type": "departure", "Pushback": pushback, "Taxi": taxi, "Takeoff": takeoff, "Handoff": handoff, "Landing": None})
    
    arrival_count = 0
    for i in range(0, len(arrivals)):
        target_callsign = (airlines[arrivals[i][3].replace(" ", "")] + arrivals[i][4]).replace(" ", "")
        # for an arrival, check for landing clearance and taxi to terminal
        landing = False
        taxi = False
        for j in range(0, len(logged_instructions)):
            # departure as a subcheck
            if target_callsign in logged_instructions[j][0]:
                if len(logged_instructions[j]) >= 6 and "LAND" in logged_instructions[j][5]:
                    landing = True
                elif len(logged_instructions[j]) >= 4 and logged_instructions[j][3] in terminal_synonyms:
                    taxi = True
        
        if landing and taxi:
            arrival_count += 1
        else:
            unhandled.append({"Callsign": target_callsign, "Type": "arrival", "Pushback": None, "Taxi": taxi, "Takeoff": None, "Handoff": None, "Landing": landing})
    
    return GA_departure_count, GA_arrival_count, departure_count, arrival_count, unhandled

# Configuration
# Change as needed depending on Tower!3D Pro version and tournament conditions
print("For the next inputs, you can give 0, 1 or more answers. Enter one at a time, and press enter to confirm your choice.")
terminal_synonyms = ["TERMINAL"]
inp = input("Enter one synonyms for TERMINAL (or nothing if not applicable): ")
while inp != "":
    terminal_synonyms.append(inp)
    inp = input("Enter one synonym for TERMINAL (or nothing if not applicable): ")

banned_runways = []
inp = input("Enter all banned runways (or none if not applicable): ")
while inp != "":
    banned_runways.append(inp)
    inp = input("Enter all banned runways (or none if not applicable): ")

arrivalairportcode = input("Enter the airport code (ex. LAX): ") # airport code without kilo
airlines_filename = input("Enter the airlines filename (ex. klax_airlines.txt): ")
GA_filename = input("Enter the GA schedule filename (ex. klax_gaandlocaltraffic.txt): ")
commercial_filename = input("Enter commercial schedule filename (ex. klax_schedule.txt): ")
gamelog_filename = input("Enter the gamelog filename (ex. output_log.txt): ")

# Importing Airline Data as a dictionary (Tower!3D Pro encodes AAL as AA for example for American Airlines)
# Usage: "AA" key (weird game format) / index will return "AAL" (ICAO)
# Context: "AA" would appear in the schedule, "AAL" would appear in the actual game log
airlines = importAirlines(airlines_filename, "//")

# Importing GA Schedule data as a split list 
GA_traffic = importGATraffic(GA_filename, "//", arrivalairportcode)
GA_departures = GA_traffic[0]
GA_arrivals = GA_traffic[1]
GA_departure_count = GA_traffic[2]
GA_arrival_count = GA_traffic[3]

# Importing Commerial Schedule data as a split list
commercial_traffic = importCommercialTraffic(commercial_filename, "//" , arrivalairportcode)
departures = commercial_traffic[0]
arrivals = commercial_traffic[1]
departure_count = commercial_traffic[2]
arrival_count = commercial_traffic[3]

# Importing commands given by user through game log
logged_instructions = importGameLog(gamelog_filename)

# Calculate and store the amount of aircraft handled
handled_aircraft = calculateHandledAircraft(logged_instructions, GA_departures, GA_arrivals, departures, arrivals, airlines, terminal_synonyms, banned_runways)
GA_departures_handled = handled_aircraft[0]
GA_arrivals_handled = handled_aircraft[1]
departures_handled = handled_aircraft[2]
arrivals_handled = handled_aircraft[3]
unhandled = handled_aircraft[4]

print()
print("Runtime Results - " + time.strftime("%H:%M:%S"))
print("Terminal Synonyms: " + str(terminal_synonyms))
print("Banned Runways: " + str(banned_runways))
print("Airport Code: " + arrivalairportcode)
print("Files used: " + airlines_filename + ", " + GA_filename + ", " + commercial_filename + ", " + gamelog_filename)
print()

print("# Airline Traffic Statistics")
print("Expected departures: " + str(departure_count) + " (" + str(departures_handled) + " handled)")
print("Expected arrivals: " + str(arrival_count) + " (" + str(arrivals_handled) + " handled)")
print()

print("# GA Traffic Statistics")
print("Expected departures: " + str(GA_departure_count) + " (" + str(GA_departures_handled) + " handled)")
print("Expected arrivals: " + str(GA_arrival_count) + " (" + str(GA_arrivals_handled) + " handled)")
print()

print("Total Runtime (ms): " + str((time.time() - initialtime) * 1000)[:6])
print()

input("Press enter to proceed view planes not considered handled... ")
print()

for i in range(0, len(unhandled)):
    print(unhandled[i])

print()
print("Execution has finished. Script will auto-close in 60 seconds...")
time.sleep(60)