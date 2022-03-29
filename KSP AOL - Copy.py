import math
import time
import krpc

conn = krpc.connect(
    name='Default Server',
    address='192.168.56.1', #192.168.56.1
    rpc_port=50000, stream_port=50001)

vessel = conn.space_center.active_vessel

target_altitude = 400
landing_altitude = 200
land_altitude = 120
TouchDown = False
landing = False
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

vessel.control.sas = False
vessel.control.rcs = True
vessel.control.throttle = 1.0

print('T-3')
time.sleep(1)
print('T-2')
time.sleep(1)
print('T-1')
time.sleep(1)
print('T-0')

vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)

obt_frame = vessel.orbit.body.non_rotating_reference_frame
obt_speed = vessel.flight(obt_frame).speed

srbs_separated = False
turn_angle = 0

while altitude() < target_altitude:
    pass
vessel.control.throttle = 0.05
print("vessel.control.throttle = 0.5")
landing = True

if landing == True:
    while altitude() < landing_altitude:
        pass
    vessel.control.throttle = 0.8
    print("vessel.control.throttle = 0.8")
if obt_speed < 5:
    vessel.control.throttle = 0.0
    
    if altitude() < land_altitude:
        vessel.control.throttle = 0
        print("vessel.control.throttle = 0 \n We Have Touch Down!!!")
        