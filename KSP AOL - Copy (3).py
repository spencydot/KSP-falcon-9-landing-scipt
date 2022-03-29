import math
import time
import krpc

conn = krpc.connect(
    name='Default Server',
    address='192.168.56.1', #192.168.56.1
    rpc_port=50000, stream_port=50001)

vessel = conn.space_center.active_vessel

target_altitude = 2000
landing_altitude = 200
land_altitude = 120
TouchDown = False
landing = False
Val = False
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')

vessel.control.sas = False
vessel.control.rcs = True
vessel.control.throttle = 0.3
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)

srbs_separated = False
turn_angle = 0

print("LAUNCH")
while altitude() <= target_altitude:
    pass
vessel.control.throttle = 0

print("Main Engine Shutdown")
while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 2:
    pass
time.sleep(2)
landing = True

print("Auto Landing Procedure T-0.3")
time.sleep(0.1)
print("Auto Landing Procedure T-0.2")
time.sleep(0.1)
print("Auto Landing Procedure T-0.1")
time.sleep(0.1)
print("Auto Landing Procedure T-0.0")

print("Speed: " , int(vessel.flight(vessel.orbit.body.reference_frame).speed) , "m/s ")

time.sleep(2)
if landing == True:
    while True:

        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 10:  
            vessel.control.throttle = 0.3
            print("Speed: " , int(vessel.flight(vessel.orbit.body.reference_frame).speed) , "m/s ")
       
        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) <= 3: 
            vessel.control.throttle = 0.1
            print("Speed: " , int(vessel.flight(vessel.orbit.body.reference_frame).speed) , "m/s ")
     
        if altitude() <= 5:
            vessel.control.throttle = 0.1
            time.sleep(0.01)
            vessel.control.throttle = 0.0
            print("Speed: " , int(vessel.flight(vessel.orbit.body.reference_frame).speed) , "m/s \nTouch Down Confirm!!\nTouch Down Confirm!!\nTouch Down Confirm!!\nTouch Down Confirm!!\nTouch Down Confirm!!")
            break