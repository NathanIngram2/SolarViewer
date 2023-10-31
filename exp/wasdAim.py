import keyboard as kb
import time
import RPi.GPIO as GPIO

from ...Python.dataCollection import measPower

# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# board and pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

print("Enter w-a-s-d for respective movement of the antenna direction.")
print("W: increase altitude, A: rotate CCW, S: decrease altitude, D: rotate CW")

try:
    while 1:
        while kb.is_pressed('w'):
            GPIO.output(DIR,CW)
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            time.sleep(.005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            time.sleep(.005) # Dictates how fast stepper motor will run

        while kb.is_pressed('a'):
            GPIO.output(DIR, CCW)
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            time.sleep(.005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            time.sleep(.005) # Dictates how fast stepper motor will run

        while kb.is_pressed('s'):
            GPIO.output(DIR, CCW)
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            time.sleep(.005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            time.sleep(.005) # Dictates how fast stepper motor will run

        while kb.is_pressed('d'):
            GPIO.output(DIR, CW)
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            time.sleep(.005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            time.sleep(.005) # Dictates how fast stepper motor will run

        if kb.is_pressed('m'):
            freq_min = int(input("What is the min frequency?"))
            freq_max = int(input("What is the max frequency?"))
            integration_interval = int(input("How long would you like this averaged over (reccomended <3sec)"))
            measPower(freq_min, freq_max, integration_interval)

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()
    