import math
import time
import krpc

conn = krpc.connect(
    name='Default Server',
    address='192.168.56.1', #192.168.56.1
    rpc_port=50000, stream_port=50001)

vessel = conn.space_center.active_vessel

target_altitude = 200
TouchDown = False
landing = False
Val = False
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')

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


while altitude() <= target_altitude:
    pass
vessel.control.throttle = 0

vessel.control.brakes = True
while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 2:
    pass
time.sleep(2)

while altitude() <= (target_altitude / 2 * 0.5):
    pass
landing = True

while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 5:
    vessel.control.throttle = 0.9
    pass

if landing == True:
    while True:
        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 5:  
            vessel.control.throttle = 0.3
  
        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) <= 3: 
            vessel.control.throttle = 0.1

        if int(altitude()) <= 5:
            vessel.control.throttle = 0.5
            time.sleep(0.4)
            vessel.control.throttle = 0.0
            vessel.control.brakes = False
            break

        if altitude() <= 45:
            vessel.control.gear = True
            vessel.control.lights = False
        else:
            vessel.control.gear = False
            vessel.control.lights = True