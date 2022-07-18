import time, os
from tkinter import *
from tkinter import filedialog
import webbrowser

initialtime = time.time()

def setupGUI():
    global l1ent, l2ent, l3ent, l4ent, l5ent, l6ent, l7ent, teamname, open_after, data, root
    l1ent = l2ent = l3ent = l4ent = l5ent = l6ent = l7ent = open_after = data = None
    root = Tk()
    root.title("Tower 3D Log Grader V0.2.0")
    x = 500
    y = 800
    root.geometry(str(x) + "x" + str(y))
    root.resizable(False, False)
    root.configure(background="white")
    title_preset = ("Calibri", 18, "bold")
    subtitle_preset = ("Calibri", 15, "italic")
    body_preset = ("Calibri", 11,)
    button_preset = ("Calibri", 10,)
    num_rows = 9
    teamname = "default" # not yet implemented

    class uploadButton():
        def __init__(self, root, x, y, row, column, font, preferredname):
            self.root = root
            self.x = X
            self.y = y
            self.color = "red"
            self.row = row
            self.column = column
            self.font = font
            self.button = Button(root, bg=self.color, text="Click to browse... ", command=self.openfile, font=self.font)
            self.button.grid(row=self.row, column=0)
            self.path = None
            self.preferredname = preferredname

        def openfile(self):
            file = filedialog.askopenfile(mode='r')
            if file:
                self.path = os.path.abspath(file.name)
                if self.preferredname in self.path:
                    self.color = "green"
                else:
                    self.color = "orange"
                self.label = self.path.split("\\")[-1]
                self.rebuild()

        def rebuild(self):
            self.button.destroy()
            self.button = Button(self.root, bg=self.color, text=self.label, command=self.openfile)
            self.button.grid(row=self.row, column=0)
        
        def getPath(self):
            return self.path

    l0 = Label(root, text="Configuration", background="white", font=title_preset)
    l0.grid(row = 0, column = 0, sticky = W, pady = 2)

    l1 = Label(root, text="Terminal Synonyms: ", background="white", font=subtitle_preset)
    l1.grid(row = 1, column = 0, sticky = W, pady = 2)
    l1sub = Label(root, text="Comma separated synonyms for terminal ex: TERMINAL, RAMP, APRON", background="white", font=body_preset)
    l1sub.grid(row = 2, column = 0, sticky = W, pady = 2)
    l1ent = Entry(root)
    l1ent.insert(0, "TERMINAL, APRON, RAMP")
    l1ent.grid(row=3, column=0)

    l2 = Label(root, text="Banned Runways: ", background="white", font=subtitle_preset)
    l2.grid(row = 4, column = 0, sticky = W, pady = 2)
    l2sub = Label(root, text="Comma separated runways ex: 24R, 25R", background="white", font=body_preset)
    l2sub.grid(row = 5, column = 0, sticky = W, pady = 2)
    l2ent = Entry(root)
    l2ent.grid(row=6, column=0)

    l3 = Label(root, text="Airport code ex: LAX: ", background="white", font=subtitle_preset)
    l3.grid(row = 7, column = 0, sticky = W, pady = 2)
    l3sub = Label(root, text="3 letter IATA Airport code ex: LAX ", background="white", font=body_preset)
    l3sub.grid(row = 8, column = 0, sticky = W, pady = 2)
    l3ent = Entry(root)
    l3ent.grid(row=9, column=0)
    
    l4 = Label(root, text="Airlines file (????_airlines.txt) ", background="white", font=subtitle_preset)
    l4.grid(row = 10, column = 0, sticky = W, pady = 2)
    l4ent = uploadButton(root, 0, 0, 11, 0, button_preset, "_airlines")

    l5 = Label(root, text="General Aviation Schedule (????_gaandlocaltraffic.txt) ", background="white", font=subtitle_preset)
    l5.grid(row = 13, column = 0, sticky = W, pady = 2)
    l5ent = uploadButton(root, 0, 0, 14, 0, button_preset, "_gaandlocaltraffic")

    l6 = Label(root, text="Commercial Schedule (????_schedule.txt) ", background="white", font=subtitle_preset)
    l6.grid(row = 15, column = 0, sticky = W, pady = 2)
    l6ent = uploadButton(root, 0, 0, 16, 0, button_preset, "_schedule")

    l7 = Label(root, text="Output Log (output_log.txt) ", background="white", font=subtitle_preset)
    l7.grid(row = 18, column = 0, sticky = W, pady = 2)
    l7ent = uploadButton(root, 0, 0, 19, 0, button_preset, "output_log")
    
    # unimplemented checkbox option to open the file after analysis completion
    """l8 = Label(root, text="Other configs: ", background="white", font=subtitle_preset)
    l8.grid(row = 20, column = 0, sticky = W, pady = 2)
    l8ent = Checkbutton(root, text="Open file after completion", background="white", variable=open_after, onvalue=True, offvalue=False)
    l8ent.grid(row=21, column=0)"""

    def endGUI():
        global l1ent, l2ent, l3ent, l4ent, l5ent, l6ent, l7ent, teamname, open_after, data, root
        data = l1ent.get().split(", "), l2ent.get().split(", "), l3ent.get(), l4ent.getPath(), l5ent.getPath(), l6ent.getPath(), l7ent.getPath(), teamname, open_after
        root.destroy()
    
    lf = Button(root, command=endGUI, text="Start", background="blue", foreground="white")
    lf.grid(row=22, column=0)

    root.mainloop()


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
    last_time = ""
    for i in range(len(logfile_contents)-1, 0, -1):
        if "alt" in logfile_contents[i]:
            last_time = logfile_contents[i][0:8]
            break
    for i in range(0, len(logfile_contents)):
        if logfile_contents[i][0:8] == "COMMAND:":
            fullinstruction = logfile_contents[i][10:].split(" ")
            if len(fullinstruction) >= 3:
                logged_instructions.append(logfile_contents[i][10:].split(" "))
        elif "PARSE CMD: " in logfile_contents[i]:
            fullinstruction = logfile_contents[i][(logfile_contents[i].index("PARSE CMD: ")):].split(" ")
            fullinstruction.insert(0, logfile_contents[i][logfile_contents[i].index("*")+2:logfile_contents[i].index("=")-1])
            fullinstruction.remove("PARSE")
            fullinstruction.remove("CMD:")
            fullinstruction.remove("")
            logged_instructions.append(fullinstruction)
    return logged_instructions, last_time

def calculateHandledAircraft(logged_instructions, GA_departures, GA_arrivals, departures, arrivals, airlines, terminal_synonyms, banned_runways):
    GA_departure_stats = {}
    GA_arrival_stats = {}
    departure_stats = {}
    arrival_stats = {}

    go_arounds = 0

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
                elif len(logged_instructions[j]) >= 4 and logged_instructions[j][3].replace("\n", "") in terminal_synonyms:
                    taxi = True
                elif len(logged_instructions[j]) >= 3 and logged_instructions[j][1] == "GO" and "AROUND" in logged_instructions[j][2]:
                    go_arounds += 1
        if landing and taxi:
            arrival_count += 1
        else:
            unhandled.append({"Callsign": target_callsign, "Type": "arrival", "Pushback": None, "Taxi": taxi, "Takeoff": None, "Handoff": None, "Landing": landing})
    return GA_departure_count, GA_arrival_count, departure_count, arrival_count, unhandled, GA_departure_stats, GA_arrival_stats, departure_stats, arrival_stats, go_arounds

if __name__ == "__main__":
    # Configuration
    setupGUI()
    terminal_synonyms = data[0]
    banned_runways = data[1]
    arrivalairportcode = data[2]
    airlines_filename = data[3]
    GA_filename = data[4]
    commercial_filename = data[5]
    gamelog_filename = data[6]
    teamname = data[7]
    open_after = data[8]

    output_file_path = teamname + "-" + arrivalairportcode + "-auto.log"
    output_file = open(output_file_path, "x")

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
    logged_instructions = importGameLog(gamelog_filename)[0]
    last_time = importGameLog(gamelog_filename)[1]

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
    go_arounds = handled_aircraft[9]

    output_file.write("Runtime Results - autograder - " +  time.strftime("%H:%M:%S") + "\n")
    output_file.write("\n")

    output_file.write("# Configuration\n")
    
    output_file.write("Terminal Synonyms: " + str(terminal_synonyms)+ "\n")
    output_file.write("Banned Runways: " + str(banned_runways)+ "\n")
    output_file.write("Airport Code: " + arrivalairportcode + "\n")
    output_file.write("Files used: " + airlines_filename + ", " + GA_filename + ", " + commercial_filename + ", " + gamelog_filename + "\n")
    output_file.write("\n")

    output_file.write("Please Note: For the runway usage statistics, only the first clearance is measured for each plane and only allowed runways are counted\n")
    output_file.write("\n")

    output_file.write("# Airline Traffic Statistics\n")
    output_file.write("Expected departures: " + str(departure_count) + " (" + str(departures_handled) + " handled)\n")
    output_file.write("Expected arrivals: " + str(arrival_count) + " (" + str(arrivals_handled) + " handled)\n")
    output_file.write("\n")

    output_file.write("# GA Traffic Statistics\n")
    output_file.write("Expected departures: " + str(GA_departure_count) + " (" + str(GA_departures_handled) + " handled)\n")
    output_file.write("Expected arrivals: " + str(GA_arrival_count) + " (" + str(GA_arrivals_handled) + " handled)\n")
    output_file.write("\n")

    output_file.write("# Unhandled planes\n")

    for i in range(0, len(unhandled)):
        output_file.write(str(unhandled[i]) + "\n")
    output_file.write("\n")

    def getDictKeysList(dict):
        # somewhat dodgy way of getting the keys of a dict as a list
        keysList = str(dict.keys())[11:-2].split(", ")
        for i in range(0, len(keysList)):
            keysList[i] = keysList[i].replace("'", "")
        return keysList

    output_file.write("# Runway Usage Statistics (number of flights which were assigned the runway / total handled)\n")

    departure_message = "Commercial - departures: "
    departure_runwaykeys = getDictKeysList(departure_stats)
    remainder = departure_count
    try:
        for i in range(0, len(departure_runwaykeys)):
            departure_message += "RWY" + departure_runwaykeys[i] + " - " + str(departure_stats[departure_runwaykeys[i]]) + "/" + str(departure_count) + " (" + str((departure_stats[departure_runwaykeys[i]]/departure_count)*100)[0:6] + "%) "
            remainder -= int(departure_stats[departure_runwaykeys[i]])
        departure_message += "Unhandled: " + str(remainder) + " (" + str(remainder / departure_count)[0:6] + "%)"
        output_file.write(departure_message + "\n")
    except:
        pass

    arrival_message = "Commercial - arrivals: "
    arrival_runwaykeys = getDictKeysList(arrival_stats)
    remainder = arrival_count
    for i in range(0, len(arrival_runwaykeys)):
        arrival_message += "RWY" + arrival_runwaykeys[i] + " - " + str(arrival_stats[arrival_runwaykeys[i]]) + "/" + str(arrival_count) + " (" + str((arrival_stats[arrival_runwaykeys[i]]/arrival_count)*100)[0:6] + "%) "
        remainder -= int(arrival_stats[arrival_runwaykeys[i]])
    arrival_message += "Unhandled: " + str(remainder) + " (" + str(remainder / arrival_count)[0:6] + "%)"
    output_file.write(arrival_message + "\n")

    output_file.write("\n")

    output_file.write("# Session Stats\n")
    output_file.write("Last time: " + last_time + "\n")
    output_file.write("Go arounds: " + str(go_arounds) + "\n")
    output_file.write("\n")
    output_file.write("Total Runtime (ms): " + str((time.time() - initialtime) * 1000)[:6] + "\n")

    print(open_after)
    if open_after:
        webbrowser.open(output_file)