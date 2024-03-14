"""
File: wasdAim.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-11-25
Description: Aim utilities for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.

Copyright (C) 2023  Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from getch import getch
import time
import RPi.GPIO as GPIO

from measPower_dummy import measPower

# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
DIR_AZ = 10 # Azimuth stepper motor direction pin from controller
STEP_AZ = 8 # Azimuth stepper motor pin from controller
DIR_ALT = 13 # Altitude stepper motor direction pin from controller
STEP_ALT = 15 # Altitude stepper motor direction pin from controller

# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

STEP_SIZE = 0.45
EL_GEAR_RATIO = 10
AZ_GEAR_RATIO = 4.4

DEGREES_EL = STEP_SIZE/EL_GEAR_RATIO
DEGREES_AZ = STEP_SIZE/AZ_GEAR_RATIO

# board and pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DIR_AZ, GPIO.OUT)
GPIO.setup(STEP_AZ, GPIO.OUT)
GPIO.setup(DIR_ALT, GPIO.OUT)
GPIO.setup(STEP_ALT, GPIO.OUT)

print("Enter w-a-s-d for respective movement of the antenna direction.")
print("W: increase altitude, A: rotate CCW, S: decrease altitude, D: rotate CW")
zeroPoint = False

while True:

    keyPressed = getch()

    if keyPressed == 'z':
        zeroPoint = True
        az = 0
        alt = 0
        print("Reached Zero Point")

    if keyPressed == 'w':
        print("Increasing altitude")
        if zeroPoint == True:
                alt = alt + DEGREES_EL
                print("Updated location: Alt = " + str(alt) + " Az = " + str(az))
        GPIO.output(DIR_ALT,CW)
        # Set one coil winding to high
        GPIO.output(STEP_ALT,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.001) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP_ALT,GPIO.LOW)
        time.sleep(.001) # Dictates how fast stepper motor will run

    if keyPressed == 'a':
        print("CCW rotation")
        if zeroPoint == True:
                az = az - DEGREES_AZ
                print("Updated location: Alt = " + str(alt) + " Az = " + str(az))
        GPIO.output(DIR_AZ, CW)
        # Set one coil winding to high
        GPIO.output(STEP_AZ,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.001) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP_AZ,GPIO.LOW)
        time.sleep(.001) # Dictates how fast stepper motor will run

    if keyPressed == 's':
        print("Decreasing altitude")
        if zeroPoint == True:
                alt = alt - DEGREES_EL
                print("Updated location: Alt = " + str(alt) + " Az = " + str(az))
        GPIO.output(DIR_ALT, CCW)
        # Set one coil winding to high
        GPIO.output(STEP_ALT,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.001) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP_ALT,GPIO.LOW)
        time.sleep(.001) # Dictates how fast stepper motor will run

    if keyPressed == 'd':
        print("CW rotation")
        if zeroPoint == True:
                az = az + DEGREES_AZ
                print("Updated location: Alt = " + str(alt) + " Az = " + str(az))
        GPIO.output(DIR_AZ, CCW)
        # Set one coil winding to high
        GPIO.output(STEP_AZ,GPIO.HIGH)
        # Allow it to get there.
        time.sleep(.001) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP_AZ,GPIO.LOW)
        time.sleep(.001) # Dictates how fast stepper motor will run

    if keyPressed == 'm':
        freq_min = input("What is the min frequency?") + "M"
        freq_max = input("What is the max frequency?") + "M"
        integration_interval = input("How long would you like this averaged over (recomended <3sec)") + "s"
        measPower(freq_min, freq_max, integration_interval)

    if keyPressed == 'n':
        freq_min = "980M"
        freq_max = "1020M"
        integration_interval = "1s"
        measPower(freq_min, freq_max, integration_interval)

    if keyPressed == 'b':
        break

print("cleanup")
GPIO.cleanup()
    
