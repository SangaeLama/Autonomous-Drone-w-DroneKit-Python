print "Initialising..."

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
import math
import time

# Connect to the Vehicle.
print("Connecting to vehicle on 127.0.0.1:14550")
vehicle = connect('127.0.0.1:14550', wait_ready=True)

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

curr_location = LocationGlobalRelative(27.707566, 85.325082,20)
a_location = LocationGlobalRelative(27.708243, 85.324692, 20)
distance=get_distance_metres(curr_location, a_location)
print ("The mission distance is"+ str(distance))

#Go to the target location, use simple goto until the distance from the target is at least 2m
while distance >= 1:
	vehicle.simple_goto(LocationGlobalRelative(27.708243, 85.324692,20))
	curr_location = vehicle.location.global_frame
	distance=get_distance_metres(curr_location, a_location)
	time.sleep(4)
	print ("FLying at height of ", str(vehicle.location.global_frame.alt))
	print("--------The remaining distance is "+ str(distance))

vehicle.mode = VehicleMode("LOITER")
print ("Loitering for 10 seconds...")
time.sleep(10)
print ("The altitude is ")
altd = vehicle.location.global_frame.alt
print (altd)
vehicle.mode = VehicleMode("LAND")
while altd >= 0:
    time.sleep(1)
    altd = vehicle.location.global_frame.alt
    print ("The current altitude of the drone is "+ str(altd))
    	
print("Landing complete... Disarming motors now...")
time.sleep(3)
vehicle.armed = False

print("------------------Mission Complete ------------------")

response=input("Do you wish to continue???")
if response=="y" or "Y" or "Yes" or "yes":
    print ("continuing...")

print ("........Mission complete.......")

# # Shut down simulator
#sitl.stop()
# print("Completed")

