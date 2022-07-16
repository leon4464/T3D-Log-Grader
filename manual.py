import time
from auto import importGameLog

gamelog_data = importGameLog(input("Enter the gamelog filename (ex. output_log.txt): "))
airlines = gamelog_data[0]

target_plane = input("Enter the name of the plane you'd like to find clearances for (ex. SWA1904): ")

initialtime = time.time()

for i in range(len(airlines)):
    if airlines[i][0] == target_plane:
        print(airlines[i])
print()

print("Total Processing Time (ms): " + str((time.time() - initialtime) * 1000)[:6])
print()