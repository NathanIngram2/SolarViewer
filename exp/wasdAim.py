from getch import getch
import time
import RPi.GPIO as GPIO

#from ...Python.dataCollection import measPower

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

while True:

    keyPressed = getch()

    if keyPressed == 'w':
        print("Increasing altitude")
        GPIO.output(DIR,CW)
        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.005) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        time.sleep(.005) # Dictates how fast stepper motor will run

    if keyPressed == 'a':
        print("CCW rotation")
        GPIO.output(DIR, CCW)
        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.005) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        time.sleep(.005) # Dictates how fast stepper motor will run

    if keyPressed == 's':
        print("Decreasing altitude")
        GPIO.output(DIR, CCW)
        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.005) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        time.sleep(.005) # Dictates how fast stepper motor will run

    if keyPressed == 'd':
        print("CW rotation")
        GPIO.output(DIR, CW)
        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.005) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        time.sleep(.005) # Dictates how fast stepper motor will run

    if keyPressed == 'm':
        freq_min = int(input("What is the min frequency?"))
        freq_max = int(input("What is the max frequency?"))
        integration_interval = int(input("How long would you like this averaged over (reccomended <3sec)"))
        #measPower(freq_min, freq_max, integration_interval)

    if keyPressed == 'b':
        break

print("cleanup")
GPIO.cleanup()
    
