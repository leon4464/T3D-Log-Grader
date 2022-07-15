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
    GA_departure_stats = {}
    GA_arrival_stats = {}
    departure_stats = {}
    arrival_stats = {}

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
                    # to avoid takeoffs being counted twice for one plane, only the first is counted (the first makes takeoff True)
                    if takeoff == False:
                        runway_used = logged_instructions[j][2][0:3] # returns runway name ie 25R, without sometimes present \n
                        # check if runway already is in the stats
                        alreadyExists = False
                        for i in departure_stats.keys():
                            if runway_used == i:
                                alreadyExists = True
                        if alreadyExists == True:
                            departure_stats[runway_used] += 1
                        else:
                            departure_stats[runway_used] = 1
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
                    # to avoid landings being counted twice for one plane, only the first is counted (the first makes landings True)
                    if landing == False:
                        runway_used = logged_instructions[j][2][0:3] # returns runway name ie 25R, without sometimes present \n
                        # check if runway already is in the stats
                        alreadyExists = False
                        for i in arrival_stats.keys():
                            if runway_used == i:
                                alreadyExists = True
                        if alreadyExists == True:
                            arrival_stats[runway_used] += 1
                        else:
                            arrival_stats[runway_used] = 1
                    landing = True
                elif len(logged_instructions[j]) >= 4 and logged_instructions[j][3] in terminal_synonyms:
                    taxi = True
        
        if landing and taxi:
            arrival_count += 1
        else:
            unhandled.append({"Callsign": target_callsign, "Type": "arrival", "Pushback": None, "Taxi": taxi, "Takeoff": None, "Handoff": None, "Landing": landing})
    
    return GA_departure_count, GA_arrival_count, departure_count, arrival_count, unhandled, GA_departure_stats, GA_arrival_stats, departure_stats, arrival_stats 

# Configuration
# Change as needed depending on Tower!3D Pro version and tournament conditions
terminal_synonyms = ["TERMINAL", "RAMP", "APRON"] # possible names for taxiing to final spot
banned_runways = ["24R"] # list of runways disallowed for departure / arrivals
arrivalairportcode = "LAX" # airport code without kilo
airlines_filename = "klax_airlines.txt" 
GA_filename = "klax_gaandlocaltraffic.txt"
commercial_filename = "klax_schedule.txt"
gamelog_filename = "output_log.txt"

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
GA_departure_stats = handled_aircraft[5]
GA_arrival_stats = handled_aircraft[6]
departure_stats = handled_aircraft[7]
arrival_stats = handled_aircraft[8]

print()
print("Runtime Results - " + time.strftime("%H:%M:%S"))
print("Terminal Synonyms: " + str(terminal_synonyms))
print("Banned Runways: " + str(banned_runways))
print("Airport Code: " + arrivalairportcode)
print("Files used: " + airlines_filename + ", " + GA_filename + ", " + commercial_filename + ", " + gamelog_filename)
print()

print("Please Note: For the runway usage statistics, only the first clearance is measured for each plane.")
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

input("Press enter to view planes not considered handled... ")
print()

for i in range(0, len(unhandled)):
    print(unhandled[i])
print()

input("Press enter to view runway usage stats (by valid / counted clearances)... ")
print()

def getDictKeysList(dict):
    # somewhat dodgy way of getting the keys of a dict as a list
    keysList = str(dict.keys())[11:-2].split(", ")
    for i in range(0, len(keysList)):
        keysList[i] = keysList[i].replace("'", "")
    return keysList

print("# Runway Usage Statistics (number of flights which were assigned the runway / total handled)")

departure_message = "Commercial - departures: "
departure_runwaykeys = getDictKeysList(departure_stats)
for i in range(0, len(departure_runwaykeys)):
    departure_message += "RWY" + departure_runwaykeys[i] + " - " + str(departure_stats[departure_runwaykeys[i]]) + "/" + str(departures_handled) + " (" + str((departure_stats[departure_runwaykeys[i]]/departures_handled)*100)[0:6] + "%) "

print(departure_message)

arrival_message = "Commercial - arrivals: "
arrival_runwaykeys = getDictKeysList(arrival_stats)
for i in range(0, len(arrival_runwaykeys)):
    arrival_message += "RWY" + arrival_runwaykeys[i] + " - " + str(arrival_stats[arrival_runwaykeys[i]]) + "/" + str(arrivals_handled) + " (" + str((arrival_stats[arrival_runwaykeys[i]]/arrivals_handled)*100)[0:6] + "%) "

print(arrival_message)