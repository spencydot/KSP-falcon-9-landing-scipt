import math
import time
import krpc
import os

conn = krpc.connect(
    name='Default Server',
    address='192.168.56.1', #192.168.56.1
    rpc_port=50000, stream_port=50001)

vessel = conn.space_center.active_vessel            #The rocket
target_altitude = 230                              #Time in space when the engine shuts off
target_e_active = (target_altitude / 2 * 0.5)       #the point where the engine activats
TouchDown = False                                   #If the rocket has landed or not
landing = False                                     #If the rocket is landing or falling
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude') #Altiude of the rocket deturmand by the center of mass
vessel.control.sas = True                           #The rocket dose not need SAS
vessel.control.rcs = True                           #The rocket dose need RCS for better mobility
vessel.control.lights = False                       #Turns the lights off while flying                        
vessel.auto_pilot.target_pitch_and_heading(90, 90)  #Make sure the rocket is flying direcrly up                          #Engages autopilot AKA this script
TakeOff = True
landed = False

def Log():         #This displayes infomation on the rocket
    print(" Lights:             ", vessel.control.lights,"\n",
    "Gear:               ",vessel.control.gear,"\n",
    "Speed:              ",int(vessel.flight(vessel.orbit.body.reference_frame).speed),"\n",
    "Throtle:            ",vessel.control.throttle,"\n",
    "Altitude:           ",altitude(),"\n",
    "Target Altitude:    ",target_altitude,"\n",
    "Target E acitve:    ",target_e_active,"\n",)
    if landed == True:
        print("Touch Down!!")

def touchDown():  #this retracts the landing and exits the program
    while int(altitude()) <= 20:
        vessel.control.throttle = 0.0
        vessel.control.lights = False

def UberSlow(): #Slows the rocket to 1m/s
    while True:
        Log()
        while vessel.flight(vessel.orbit.body.reference_frame).speed >= 1:  
            vessel.control.throttle = 0.4
        while vessel.flight(vessel.orbit.body.reference_frame).speed <= 0.5: 
            vessel.control.throttle = 0.2
        os.system('cmd /c "cls"')
        if int(altitude()) <= 9:
            touchDown()

def landing(): #Slows the rocket to 5/ms
    while True:
        Log()
        if altitude() <= 45:
            vessel.control.gear = True
            vessel.control.lights = True
            TakeOff = False     

        if int(altitude()) <= 8:
            touchDown()
            break

        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <= -5:  
            vessel.control.throttle = 0.8
        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) >= -2: 
            vessel.control.throttle = 0.2

        os.system('cmd /c "cls"')

def landFar(): #Slows the rocket to 38m/s
    while True:
        Log()
        time.sleep(0.01)
        
        while altitude() <= 250:
            landing()
            break

        while vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed >= -1:
            vessel.auto_pilot.sas_mode = vessel.auto_pilot.sas_mode.retrograde
            print("Corecting for horizontal_speed")

            while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <= -21:  
                vessel.control.throttle = 0.8

            while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) >= -20: 
                vessel.control.throttle = 0.2

        while vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed >= 1:
            vessel.auto_pilot.sas_mode = vessel.auto_pilot.sas_mode.retrograde
            print("Corecting for horizontal_speed")

            while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <= -21:  
                vessel.control.throttle = 0.8

            while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) >= -20: 
                vessel.control.throttle = 0.2

        while vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed <= 0.5:
            vessel.auto_pilot.sas_mode = vessel.auto_pilot.sas_mode.stability_assist

            while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <= -21:  
                vessel.control.throttle = 0.8

            while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) >= -20: 
                vessel.control.throttle = 0.2

        os.system('cmd /c "cls"')

def Takeoff(): #Launches the rocket + belly flops
    while altitude() <= target_altitude:
        vessel.control.throttle = 1
        pass
    while altitude() >= target_altitude:
        vessel.control.throttle = 0
        while int(vessel.flight(vessel.orbit.body.reference_frame).vertical_speed) <= 2:
            time.sleep(2)
            landFar()
            break

def Launch(): #Activates first stage (Launches the rocket)
    vessel.control.activate_next_stage()
    vessel.control.gear = False     
    vessel.control.throttle = 1
    print("LAUNCH!!!")
    Log()
    Takeoff()

Launch()