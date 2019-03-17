from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

#-- Connect to the vehicle
import argparse
parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()

connection_string = args.connect


print ("Connection to the vehicle on %s"%connection_string)
print (connection_string)
vehicle = connect(connection_string, wait_ready=True)

#-- Defining function for takeoff
def arm_and_takeoff(tgt_altitude):
	print("Vehicle Arms check")
	
	while not vehicle.is_armable:
		time.sleep(1)
	
	vehicle.mode = VehicleMode("GUIDED")
	vehicle.armed = True
	print("......Armed.......")

	vehicle.simple_takeoff(tgt_altitude)
	print("The Target Altitude is %s"%tgt_altitude)
	#-- wait to reach the target altitude
	while True:
		altitude = vehicle.location.global_relative_frame.alt
		print ("The current altitude is %s"%altitude)
		#if vehicle.location.global_relative_frame.alt>=tgt_altitude*0.95:
        	#	print "Reached target altitude"
        	#	break
		if altitude >= tgt_altitude:
			print("Target Altitude Reached %s"%altitude)
			break
		time.sleep(1)
		altitude = tgt_altitude-1

#-------Main Program ------------------
arm_and_takeoff(10)

#---- set the default speed
vehicle.airspeed = 7
#---- Go To WP1
print ("Going to WP1")
wp1 = LocationGlobalRelative(27.6064423,85.3343279,10)
vehicle.simple_goto(wp1)

#---- Play here ....
time.sleep(10)

#---- Coming back
print ("Coming back...")
vehicle.mode = VehicleMode("RTL")

time.sleep(5)

#---- Close connection ---------
vehicle.close()


