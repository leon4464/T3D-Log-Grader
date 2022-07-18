# Tower 3D! Pro Log Grader :airplane: :small_airplane:

This Python script allows you to grade logs of Tower 3D! Pro sessions. This is intended for situations like tournaments or competitions. It was originally built for a Tower! 3D Pro tournament held in July of 2022.

## Basic functionality
- Provides a *score report* useful in determining a final score for a competition
- Allows you to configure banned runways (they won't be counted as a valid departure / arrival if they are "banned").
- Allows you to easily configure a challenge with the GUI
- Allows you to manually and quickly find all commands relating to an aircraft manually if so desired with manual.py
- Compatible with Eligrim's tower3d.rec mod by default (currently unofficially tested)
- The use of this app is not intended as standalone - you should also collect time & score in the form of a screenshot from the host
> In theory, a user could issue a landing & taxi clearance while a plane is in the air - and the program would consider it a "handled" arrival - so it is recommended to use this alongside a screenshot of the points (so you can be sure everything was properly handled). 

# Usage and requirements
- Use Python 3.9.13 or later
- The output_log.txt created after a (single or multiplayer) session of Tower!3D Pro (latest version as of 13.07.2022 is supported)
- The schedule files for general aviation and commercial aircraft (ie *klax_gaandlocaltraffic.txt* and *klax_schedule.txt*)
- The airlines file (ie *klax_airlines.txt*)
- By default the script will output file (which will be generated in the same directory of auto.py) something like:

```
Runtime Results - 23:41:46
Terminal Synonyms: ['TERMINAL', 'RAMP', 'APRON']
Banned Runways: ['24R']
Airport Code: LAX
Files used: {removed filepath!}, {removed filepath!}, {removed filepath!}, {removed filepath!}

Please Note: For the runway usage statistics, only the first clearance is measured for each plane.

# Airline Traffic Statistics
Expected departures: 60 (58 handled)
Expected arrivals: 66 (66 handled)

# GA Traffic Statistics
Expected departures: 0 (0 handled)
Expected arrivals: 0 (0 handled)

Total Runtime (ms): 16.003

Press enter to view planes not considered handled...

{'Callsign': 'ITY621', 'Type': 'departure', 'Pushback': True, 'Taxi': False, 'Takeoff': False, 'Handoff': False, 'Landing': None}
{'Callsign': 'SWA1904', 'Type': 'departure', 'Pushback': False, 'Taxi': True, 'Takeoff': False, 'Handoff': False, 'Landing': None}

Press enter to view runway usage stats (by valid / counted clearances)...

# Runway Usage Statistics (number of flights which were assigned the runway / total handled)
Commercial - departures: RWY25R - 32/58 (55.172%) RWY24L - 26/58 (44.827%)
Commercial - arrivals: RWY24R - 37/66 (56.060%) RWY25R - 29/66 (43.939%)
```

# Known issues
- [ ] Implementation of GA aircraft is **not yet implemented**
- [ ] Inefficiencies in the code (checking a potentially invalid departure / arrival multiple times).
- [ ] GA aircraft haven't been fully and may be counted incorrectly.
- [ ] Banning runways isn't fully tested and has issues

# Customisation of the application
## Banning runways
- Add the name of the runway (for example "24R") in the config GUI and no departure / arrival using this will be considered "handled".
## How to write custom checks
- Need to edit the script, and you can only look for keywords in commands (you could ban go arounds for instance)

# Contributing to this repository
- This repository is open to contributions either in or not in the known issues.

# Acknowledgements
The following were extremely useful in creating this project:
- Eligrim's various Tower 3D! Pro tools (https://eligrim.de/)
- ATC Suite's Tower 3D! Pro manual (https://www.atcsuite.com/tower-promanual)
