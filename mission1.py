print "Start simulator (SITL)"
#import dronekit_sitl
import time
#sitl = dronekit_sitl.start_default()

import argparse
parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()

connection_string = args.connect

#connection_string = sitl.connection_string()

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import math
#import dronekit
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect('127.0.0.1:14550', wait_ready=True)

"""
# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable
"""

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)

VajraSchool = 27.6064423,85.3343279
curr_location = LocationGlobalRelative(27.608321,85.3322697,20)
earth_radius = 6378137.0 #Radius of "spherical" earth
#Coordinate offsets in radians
dLat = 27.6064423
dLon = 85.3343279
dNorth = dLat*earth_radius
dEast = dLon*(earth_radius*math.cos(math.pi*curr_location.lat/180))



def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5





arm_and_takeoff(10)


home = 27.608321,85.3322697
VajraSchool = 27.6064423,85.3343279
curr_location = LocationGlobalRelative(27.608321,85.3322697,20)
a_location = LocationGlobalRelative(27.6064423,85.3343279, 20)
distance=get_distance_metres(curr_location, a_location)
print ("The distance is"+ str(distance))

while distance >= 5:
	vehicle.simple_goto(LocationGlobalRelative(27.6064423,85.3343279,10))
	curr_location = vehicle.location.global_frame
	#print ("Current location is" + str(curr_location))
	distance=get_distance_metres(curr_location, a_location)
	time.sleep(4)
	print( )
	print("--------The remaining distance is "+ str(distance))

vehicle.mode = VehicleMode("LOITER")
print ("Loitering for 10 seconds...")
time.sleep(10)
vehicle.mode = VehicleMode("LAND")
vehicle.armed = False

print("------------------Mission Complete ------------------")

"""
print(">>>>>>>>>>>>>>>>>Going towards target")

vehicle.simple_goto(LocationGlobalRelative(27.608321,85.3322697,30))




print("Sleeping now... for 10 secs")

print ("Reached the target location")
#print ("30seconds for flight towards wp1 completed")

#time.sleep(30)
#vehicle.close()

vehicle.mode = VehicleMode("LAND")
print ("Landing on the target...")
vehicle.armed = False

print ("........Mission complete.......")

# # Shut down simulator
#sitl.stop()
# print("Completed")
"""
