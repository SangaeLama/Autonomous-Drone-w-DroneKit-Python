# FYP
Humanitarian Drone w/ Dronekit
# Drone Control Script

This Python script uses DroneKit-Python to connect to a drone via network on localhost:14550. It enables you to control the drone by sending commands, performing basic actions like arming, takeoff, and waypoint navigation, and provides functions to calculate distances and bearings between locations.

## Prerequisites

- [DroneKit-Python](https://github.com/dronekit/dronekit-python) installed.
- A real drone connected to the local network, listening on `localhost:14550`.
- Python 2.7 or higher.

## Usage

1. Ensure your real drone is powered on and connected to the local network.

2. Clone or download this repository to your local machine.

3. Open a terminal and navigate to the project directory.

4. Modify the `connection_string` variable in the script to match your drone's connection string.

5. Run the script using the following command:

   ```bash
   python mission.py
