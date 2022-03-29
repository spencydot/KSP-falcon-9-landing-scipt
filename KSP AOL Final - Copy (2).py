import math
import time
import krpc
import os
  
conn = krpc.connect(
    name='Default Server',
    address='192.168.56.1', #192.168.56.1
    rpc_port=50000, stream_port=50001)

vessel = conn.space_center.active_vessel                                  #   The rocket
target_altitude = 260                                                     #   Time in space when the engine shuts off
target_e_active = (target_altitude / 2 * 0.5)                             #   the point where the engine activats
TouchDown = False                                                         #   If the rocket has landed or not
landing = False                                                           #   If the rocket is landing or falling
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')  #   Altiude of the rocket deturmand by the center of mass
vessel.control.sas = False                                                #   The rocket dose not need SAS
vessel.control.rcs = True                                                 #   The rocket dose need RCS for better mobility
vessel.control.lights = False                                             #   Turns the lights off while flying                        
vessel.auto_pilot.target_pitch_and_heading(90, 90)                        #   Make sure the rocket is flying direcrly up                          #Engages autopilot AKA this script
vessel.auto_pilot.engage()  
TakeOff = True
landed = False
Corecting = False


def Log():         #This displayes infomation on the rocket
    print("Lights:             ", vessel.control.lights,"\n",
    "Gear:               ",vessel.control.gear,"\n",
    "Speed:              ",int(vessel.flight(vessel.orbit.body.reference_frame).speed),"\n",
    "Throtle:            ",int(vessel.control.throttle) * 10,"\n",
    "Altitude:           ",int(altitude()),"\n",
    "Target Altitude:    ",target_altitude,"\n",
    "horizontal Speed:   ",int(vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed)*10,"\n",
    "Land Corection:     ",Corecting,"\n",
    "Target E acitve:    ",target_e_active,"\n")

    f = open("demofile2.txt", "a")
    f.write("Lights:             ", vessel.control.lights,
"Gear:               ",vessel.control.gear,
"Speed:              ",int(vessel.flight(vessel.orbit.body.reference_frame).speed),
"Throtle:            ",int(vessel.control.throttle) * 10,
"Altitude:           ",int(altitude()),
"Target Altitude:    ",target_altitude,
"horizontal Speed:   ",int(vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed)*10,
"Land Corection:     ",Corecting,
"Target E acitve:    ",target_e_active)
    f.close()

def touchDown():  #this retracts the landing and exits the program
    while int(altitude()) <= 20:
        vessel.control.throttle = 0.0
        vessel.control.lights = False
        Log()
        
        break

def UberSlow(): #Slows the rocket to 1m/s
    while True:
        while vessel.flight(vessel.orbit.body.reference_frame).speed >= 1:  
            vessel.control.throttle = 0.4
        while vessel.flight(vessel.orbit.body.reference_frame).speed <= 0.5: 
            vessel.control.throttle = 0.2
        if int(altitude()) <= 9:
            touchDown()
        Log()
        
        os.system('cmd /c "cls"')

def landing(): #Slows the rocket to 5/ms
    while True:
        if altitude() <= 45:
            vessel.control.gear = True
            vessel.control.lights = True
            TakeOff = False     

        if int(altitude()) <= 8:
            touchDown()
            break

        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <=   5:  
            vessel.control.throttle = 0.8
        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) >=   2: 
            vessel.control.throttle = 0.2
        
        Log()
        os.system('cmd /c "cls"')

def landFar(): #Slows the rocket to 38m/s
    while True:
        time.sleep(0.01)
        
        while altitude() <= 250:
            landing()
            break

        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) >=   58:  
            vessel.control.throttle = 0.2
            LandCorection()
        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <=   50: 
            vessel.control.throttle = 0.8
            LandCorection()
        
        Log()
        os.system('cmd /c "cls"')

def LandCorection():
    while vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed >= 5:
        try:
            vessel.auto_pilot.sas_mode = vessel.auto_pilot.sas_mode.retrograde
            Corecting = True
            time.sleep(1)
        except:
            pass
        try:
            vessel.auto_pilot.sas_mode = vessel.auto_pilot.sas_mode.stability_assist
            vessel.auto_pilot.target_pitch_and_heading(90, 90)
            Corecting = False
            time.sleep(1)
        except:
            pass
    
    Log()
    os.system('cmd /c "cls"')

def Takeoff(): #Launches the rocket + belly flops
    while altitude() <= target_altitude:
        vessel.control.throttle = 1
        os.system('cmd /c "cls"')
        
        Log()
        pass
    while altitude() >= target_altitude:
        vessel.control.throttle = 0
        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <=   15:
            vessel.control.sas = True
            os.system('cmd /c "cls"')
            
            Log()
            landFar()
            break

def Launch(): #Activates first stage (Launches the rocket)
    
    Log()
    vessel.control.activate_next_stage()
    vessel.control.gear = False     
    vessel.control.throttle = 1
    print("LAUNCH!!!")
    Takeoff()
    os.system('cmd /c "cls"')



Launch()

