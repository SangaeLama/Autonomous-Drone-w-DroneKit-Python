#./Tools/autotest/sim_vehicle.py -v ArduCopter --custom-location=27.607504727228655,85.33357443159133,0,180 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
#

print("Initialising...")

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
from pymavlink import mavutil
import math
import time

# Connect to the Vehicle.
print("Connecting to vehicle on udp:127.0.0.1:14551")
vehicle = connect('udp:127.0.0.1:14551', wait_ready=True, timeout=60)

# ── MISSION SETTINGS ──────────────────────────────────────────────────────────
FLIGHT_ALTITUDE  = 50    # meters
LOITER_TIME      = 5     # seconds at each waypoint
WAYPOINT_RADIUS  = 2     # meters — how close to WP before moving to next

WAYPOINTS = [
    (27.606579495129083, 85.33403008562145),   # WP1
    (27.605291920386975, 85.33242062044872),   # WP2
    (27.60599843763167, 85.32937306833925),   # WP3
    (27.607596338334734, 85.33060252090175),   # WP4
]

# Home location — vehicle will return here and land
HOME = LocationGlobalRelative(
    WAYPOINTS[0][0],
    WAYPOINTS[0][1],
    FLIGHT_ALTITUDE
)

# ── FUNCTIONS ─────────────────────────────────────────────────────────────────

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode  = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f" Altitude: {alt:.1f}m")
        if alt >= aTargetAltitude * 0.95:
            print("Reached target altitude ✅")
            break
        time.sleep(1)

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    """
    dlat  = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5

def hold_position_at_altitude(lat, lon, altitude, duration):
    """
    Hold position at exact altitude using SET_POSITION_TARGET_GLOBAL_INT.
    Stays in GUIDED mode — most reliable way to hold altitude in SITL.
    Sends position command repeatedly to prevent altitude drift.
    """
    print(f"   Holding position at {altitude}m for {duration} seconds...")

    for i in range(duration):
        # Send position hold command every second
        # This is more reliable than LOITER mode for altitude holding
        msg = vehicle.message_factory.set_position_target_global_int_encode(
            0,                                          # time_boot_ms
            0, 0,                                       # target system, component
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            0b0000111111111000,                         # type_mask — position only
            int(lat  * 1e7),                            # lat
            int(lon  * 1e7),                            # lon
            altitude,                                   # alt — exact 20m
            0, 0, 0,                                    # vx, vy, vz
            0, 0, 0,                                    # afx, afy, afz
            0, 0                                        # yaw, yaw_rate
        )
        vehicle.send_mavlink(msg)

        alt = vehicle.location.global_relative_frame.alt
        print(f"   Hold {i+1}/{duration} — Alt: {alt:.1f}m")
        time.sleep(1)

def fly_to_waypoint(waypoint, wp_number, total_wps):
    """
    Fly to a waypoint, wait until reached, then hold at FLIGHT_ALTITUDE.
    """
    print(f"\n── Waypoint {wp_number}/{total_wps} ──────────────────────────")
    print(f"   Target: {waypoint.lat:.6f}, {waypoint.lon:.6f} at {waypoint.alt}m")

    # Stay in GUIDED mode throughout
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.simple_goto(waypoint)

    # Fly until within WAYPOINT_RADIUS metres
    while True:
        curr     = vehicle.location.global_frame
        distance = get_distance_metres(curr, waypoint)
        alt      = vehicle.location.global_relative_frame.alt
        spd      = vehicle.groundspeed

        print(f"   Alt: {alt:.1f}m | "
              f"Speed: {spd:.1f}m/s | "
              f"Distance to WP: {distance:.1f}m")

        if distance <= WAYPOINT_RADIUS:
            print(f"   Waypoint {wp_number} reached ✅")
            break
        time.sleep(1)

    # Hold position at exact FLIGHT_ALTITUDE — stays in GUIDED
    hold_position_at_altitude(
        waypoint.lat,
        waypoint.lon,
        FLIGHT_ALTITUDE,
        LOITER_TIME
    )

    print(f"   Resuming mission...")

def land():
    """
    Land the vehicle and disarm.
    """
    print("\n── Landing ──────────────────────────────────────────────")
    vehicle.mode = VehicleMode("LAND")

    while True:
        altd = vehicle.location.global_relative_frame.alt
        print(f"   Landing... Altitude: {altd:.1f}m")
        if altd <= 0.1:
            break
        time.sleep(1)

    print("Landing complete ✅")
    time.sleep(3)
    vehicle.armed = False
    print("Motors disarmed ✅")

# ── MAIN MISSION ──────────────────────────────────────────────────────────────

print("\n=== Mission Parameters ===")
print(f"Flight altitude : {FLIGHT_ALTITUDE}m")
print(f"Hold time       : {LOITER_TIME}s per waypoint")
print(f"Waypoints       : {len(WAYPOINTS)}")
for i, (lat, lon) in enumerate(WAYPOINTS):
    print(f"  WP{i+1}: {lat:.6f}, {lon:.6f}")
print(f"Return home     : {WAYPOINTS[0][0]:.6f}, {WAYPOINTS[0][1]:.6f}")
print("==========================\n")

# Takeoff
arm_and_takeoff(FLIGHT_ALTITUDE)

# Fly through all waypoints
total = len(WAYPOINTS)
for i, (lat, lon) in enumerate(WAYPOINTS):
    waypoint = LocationGlobalRelative(lat, lon, FLIGHT_ALTITUDE)
    fly_to_waypoint(waypoint, i + 1, total)

# Return home
print(f"\n── Returning Home ───────────────────────────────────────")
vehicle.mode = VehicleMode("GUIDED")
vehicle.simple_goto(HOME)

while True:
    curr     = vehicle.location.global_frame
    distance = get_distance_metres(curr, HOME)
    alt      = vehicle.location.global_relative_frame.alt
    print(f"   Returning home — Alt: {alt:.1f}m | Distance: {distance:.1f}m")
    if distance <= WAYPOINT_RADIUS:
        print("Home reached ✅")
        break
    time.sleep(1)

# Land at home
land()

print("\n========== Mission Complete ==========")
print(f"Visited {len(WAYPOINTS)} waypoints")
print(f"Held {LOITER_TIME}s at each at exactly {FLIGHT_ALTITUDE}m")
print(f"Returned and landed at home location")
print("======================================")

vehicle.close()
