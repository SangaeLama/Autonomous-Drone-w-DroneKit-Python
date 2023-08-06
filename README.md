#Autonomous Drone w/ Dronekit

# Drone Control Mission Script

This Python script uses DroneKit-Python to connect to a drone via network on localhost:14550. It enables you to control the drone by sending commands, performing basic actions like arming, takeoff, and waypoint navigation, and provides functions to calculate distances and bearings between locations.

## Prerequisites

- [DroneKit-Python](https://github.com/dronekit/dronekit-python) installed.
- A real drone connected to the local network, listening on `localhost:14550`.
- Python 2.7 or higher.


## Usage
1. Connect your computer to the drone's network. In my case, I had a VPS that was responsible for creating a reverse SSH tunnel from Drone's Raspberry Pi to my local computer.
2. Run the script using the following command:
```bash
python ./mission3.py
```
3. The script will establish a connection to the drone and perform the mission.

## Mission
- Arm and takeoff to a specified altitude.
- Navigate to a target location using GPS coordinates.
- Loiter in a location for a specified duration.
- Land the drone and disarm the motors.

## Customization
You can customize the script by modifying the following parameters:
- GPS coordinates for the takeoff and target locations.
- Target altitude for takeoff and loitering.
- Time duration for loitering.

## Notes
- Ensure that you have proper authorization and safety precautions in place before operating a drone.
- The script provides basic functionality and can be extended for more complex missions.

## Acknowledgments
This script is based on the DroneKit-Python library and is intended for educational and demonstration purposes.
