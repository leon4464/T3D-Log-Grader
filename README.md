# Tower 3D! Pro Log Grader :airplane: :small_airplane:

This Python script allows you to grade logs of Tower 3D! Pro sessions. This is intended for situations like tournaments or competitions. It was originally built for a Tower! 3D Pro tournament held in July of 2022.

## Basic functionality
- Provides a *score report* useful in determining a final score for a competition
- This report analyses a provided schedule and a log to determine how many flights needed to be handled, and how many were handled
- Allows you to ban runways from being used (they won't be counted as a valid departure / arrival if they are "banned").
- Compatible with Eligrim's tower3d.rec mod by default (although this is untested)
- The use of this app is not intended as standalone - you should also collect time & score in the form of a screenshot from the host
> In theory, a user could issue a landing & taxi clearance while a plane is in the air - and the program would consider it a "handled" arrival - so it is recommended to use this alongside a screenshot of the points (so you can be sure everything was properly handled). 

- The official release of this app will not simplify the process of adding scoring competitions, as they vary so greatly.

# Usage and requirements
- Adapt script as needed
- Use Python 3.9.13 or later
## Move the following to the same directory as the main script
- The output_log.txt created after a (single or multiplayer) session of Tower!3D Pro (latest version as of 13.07.2022 is supported) in the same directory as the script
- The schedule files for general aviation and commercial aircraft (ie *klax_gaandlocaltraffic.txt* and *klax_schedule.txt*) in the same directory as the script
- The airlines file (ie *klax_airlines.txt*) in the same directory as the script
- By default the script will output something like:

```
Runtime Results - 23:41:46
Terminal Synonyms: ['TERMINAL', 'RAMP', 'APRON']
Banned Runways: ['24R']
Airport Code: LAX
Files used: klax_airlines.txt, klax_gaandlocaltraffic.txt, klax_schedule.txt, output_log.txt

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
- [ ] A user could, theoretically just despawn aircraft after they have issued taxi clearance to the gate. There isn't a simple or elegant way to check that an aircraft has actually made it to the gate and "naturally" despawned.

# Customisation of the application
## Banning runways
- Add the name of the runway (for example "24R") to the banned_runways list and no departure / arrival using this will be considered "handled".
## How to write custom checks
- Essentially, modifying valid and invalid departures by checking for certain words or content in instructions (see the implementation of banned runways as a good example)
## Possible ideas for custom checks
- Wake turbulence considerations
> I'm not actually sure if Tower! 3D Pro implements this realistically or not, and if it could be easily implemented using time logic, but ensuring participants follow wake turbulence separation requirements could be an idea
- Banning of taxiways 
> This involves "not counting" a departure as valid if it used a banned taxiway. This feature might be implemented in the app in the future, though banning taxiways is hard because the program auto-completes taxi routes (for example: you might ban taxiway V but the program will assign a plane to it anyways; this app can only check if a user has explicitly assigned a 

# Contributing to this repository
- If you are making modifications to this official repository, please read through the docs first to understand what features are intended to be implemented.

# Acknowledgements
The following were extremely useful in creating this project:
- Eligrim's various Tower 3D! Pro tools (https://eligrim.de/)
- ATC Suite's Tower 3D! Pro manual (https://www.atcsuite.com/tower-promanual)
