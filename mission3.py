# mission3.py — updated for modern DroneKit
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
import math
import time

# Connect
print("Connecting to vehicle...")
vehicle = connect('udp:127.0.0.1:14551', wait_ready=True, timeout=60)
print(f"Connected — Mode: {vehicle.mode.name}")

def arm_and_takeoff(aTargetAltitude):
    """Arms vehicle and flies to aTargetAltitude."""
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(f"  Waiting for vehicle to initialise... "
              f"GPS:{vehicle.gps_0.fix_type}")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode  = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("  Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f"  Altitude: {alt:.1f}m")
        if alt >= aTargetAltitude * 0.95:
            print("Reached target altitude ✅")
            break
        time.sleep(1)

def get_distance_metres(aLocation1, aLocation2):
    """Ground distance in metres between two locations."""
    dlat  = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

# ── MISSION ───────────────────────────────────────────────────

# CMAC coordinates (matching SITL default location)
home     = LocationGlobalRelative(-35.3632611, 149.1652300, 20)
target   = LocationGlobalRelative(-35.3600000, 149.1670000, 20)

# Takeoff
arm_and_takeoff(10)

# Calculate mission distance
distance = get_distance_metres(home, target)
print(f"\nMission distance: {distance:.1f}m")
print(f"Flying to: {target.lat}, {target.lon} at {target.alt}m")

# Fly to target
print("\nFlying to target...")
while distance >= 2:
    vehicle.simple_goto(target)
    curr = vehicle.location.global_frame
    distance = get_distance_metres(curr, target)
    alt = vehicle.location.global_relative_frame.alt
    spd = vehicle.groundspeed
    print(f"  Alt: {alt:.1f}m | "
          f"Speed: {spd:.1f}m/s | "
          f"Distance remaining: {distance:.1f}m")
    time.sleep(2)

print("Target reached! ✅")

# Loiter
vehicle.mode = VehicleMode("LOITER")
print("\nLoitering for 10 seconds...")
for i in range(10):
    alt = vehicle.location.global_relative_frame.alt
    print(f"  Loiter {i+1}/10 — Alt: {alt:.1f}m")
    time.sleep(1)

# Land
print("\nLanding...")
vehicle.mode = VehicleMode("LAND")
while True:
    altd = vehicle.location.global_frame.alt
    print(f"  Altitude: {altd:.1f}m")
    if altd <= 0.1:
        break
    time.sleep(1)

print("Landing complete ✅")
time.sleep(3)

# Disarm
vehicle.armed = False
print("Motors disarmed ✅")
print("\n=== Mission Complete ===")

# Continue prompt
response = input("\nDo you wish to continue? (y/n): ")
if response.lower() in ["y", "yes"]:
    print("Continuing...")
    # Add next mission here
else:
    print("Mission ended.")

vehicle.close()
print("Done!")
