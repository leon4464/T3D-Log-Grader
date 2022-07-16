import time
from auto import importGameLog

gamelog_data = importGameLog(input("Enter the gamelog filename (ex. output_log.txt): "))
airlines = gamelog_data[0]

target_plane = input("Enter the name of the plane you'd like to find clearances for (ex. SWA1904): ")

log_name = input("Enter a name for the log file (ex. Blue): ")

initialtime = time.time()

logfile = open(log_name + "-" + target_plane + "-manual.log", "x")

logfile.write("Runtime Results - " + " manual grader - " + time.strftime("%H:%M:%S") + "\n")

logfile.write("\n")
logfile.write("# All instructions found for " + target_plane + ":\n")

for i in range(len(airlines)):
    if airlines[i][0] == target_plane:
        string_towrite = ""
        for j in range(len(airlines[i])):
            string_towrite += airlines[i][j] + " "
        string_towrite += "\n"
        logfile.write(string_towrite)

logfile.write("Total Processing Time (ms): " + str((time.time() - initialtime) * 1000)[:6])