import math
import time
import krpc

conn = krpc.connect(
    name='Default Server',
    address='192.168.56.1', #192.168.56.1
    rpc_port=50000, stream_port=50001)

vessel = conn.space_center.active_vessel

target_altitude = 200
landing_altitude = 200
land_altitude = 120
TouchDown = False
landing = False
Val = False
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

vessel.control.sas = False
vessel.control.rcs = True
vessel.control.throttle = 1.0
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)

srbs_separated = False
turn_angle = 0

###### LAUNCH #####
print("LAUNCH")
while altitude() < target_altitude:
    pass
vessel.control.throttle = 0.0

print(int(vessel.flight(vessel.orbit.body.reference_frame).speed))
print("Main Thrusters Shutdown")

landing = True
time.sleep(12)

def Close():
    while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 5:  
        vessel.control.throttle = 0.4
        print(int(vessel.flight(vessel.orbit.body.reference_frame).speed))

    while int(vessel.flight(vessel.orbit.body.reference_frame).speed) <= 3:
        vessel.control.throttle = 0.0
        print(int(vessel.flight(vessel.orbit.body.reference_frame).speed))

if landing == True:
    while True:
        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) >= 50:  
            vessel.control.throttle = 0.9            

        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) <= 3:
            vessel.control.throttle = 0.0

        while int(vessel.flight(vessel.orbit.body.reference_frame).speed) <= (int(vessel.flight(vessel.orbit.body.reference_frame).speed)/10):
            vessel.control.throttle = 0.4
            
        while int(altitude()) <= 120:
            Close()

        

