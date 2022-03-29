import math
import time
import krpc

conn = krpc.connect(
    name='Default Server',
    address='192.168.56.1', #192.168.56.1
    rpc_port=50000, stream_port=50001)

vessel = conn.space_center.active_vessel

target_altitude = 10
TouchDown = False
landing = False
Val = False
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')

One = 0.6
Two = 0.1


vessel.control.sas = False
vessel.control.rcs = True
vessel.control.lights = False
vessel.control.gear = False
vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.control.throttle = 1
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
srbs_separated = False
turn_angle = 0

print("LAUNCH")

while altitude() <= target_altitude:
    pass
vessel.control.throttle = 0
print("Main Engine Shutdown")
vessel.control.brakes = True
while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 2:
    pass
print("Auto Landing Procedure T-2")
print("Speed: " , int(vessel.flight(vessel.orbit.body.reference_frame).speed) , "m/s ")
print("Altitude:" , altitude())
time.sleep(2)

while altitude() <= (target_altitude / 5):
    pass
while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 5:
    vessel.control.throttle = 0.9
    pass
landing = True
vessel.control.brakes = False
print("Landing")
if landing == True:
    while True:
        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 5:  
            vessel.control.throttle = One

        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) <= 3: 
            vessel.control.throttle = Two
        if int(altitude()) <= 6:
            vessel.control.throttle = 0.2
            time.sleep(1)
            print("Speed: " , int(vessel.flight(vessel.orbit.body.reference_frame).speed) , "m/s \nTouch Down Confirm!!\nTouch Down Confirm!!\nTouch Down Confirm!!\nTouch Down Confirm!!\nTouch Down Confirm!!")
            vessel.control.throttle = 0.0
            vessel.control.brakes = False
            break

        if altitude() <= 40:
            vessel.control.gear = True
            vessel.control.lights = True
        else:
            vessel.control.gear = False
            vessel.control.lights = False