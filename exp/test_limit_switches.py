"""
File: test_limit_switches.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-11-25
Description: Limit switch testing for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.

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
import RPi.GPIO as GPIO
from time import sleep

DIR_AZ = 10 # Azimuth stepper motor direction pin from controller
STEP_AZ = 8 # Azimuth stepper motor pin from controller
DIR_ALT = 13 # Altitude stepper motor direction pin from controller
STEP_ALT = 15 # Altitude stepper motor direction pin from controller
CW = 1 # 0/1 used to signify clockwise or counterclockwise.
CCW = 0

LIM_ALT = 18 # Limit switch 1 input from Pi
LIM_AZ = 22 # Limit switch 2 input from Pi

# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIR_AZ, GPIO.OUT)
GPIO.setup(STEP_AZ, GPIO.OUT)
GPIO.setup(DIR_ALT, GPIO.OUT)
GPIO.setup(STEP_ALT, GPIO.OUT)
GPIO.setup(LIM_ALT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LIM_AZ, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set the first direction you want it to spin
GPIO.output(DIR_AZ, CCW) # Direction of calibration spin for azimuth stepper motor
GPIO.output(DIR_ALT, CCW) # Direction of calibration spin for altitude stepper motor

def calibrate(offset):
    """
    Calibrate the stepper motor to the limit switch and return the starting altitude and azimuth.

    :param offset: Azimuth offset in degrees.
    :return: Starting altitude and azimuth of the antenna in degrees. (0,0)
    """
    print("Starting Calibration...")
    # Altitude calibration
    while GPIO.input(LIM_ALT) != GPIO.HIGH:
        # Set one coil winding to high
        GPIO.output(STEP_ALT,GPIO.HIGH)
        # Allow it to get there.
        sleep(.005) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP_ALT,GPIO.LOW)
        sleep(.005) # Dictates how fast stepper motor will run


    sleep(5) # Dictates how fast stepper motor will run

    # Azimuth calibration
    while GPIO.input(LIM_AZ) != GPIO.HIGH:
        # Set one coil winding to high
        GPIO.output(STEP_AZ,GPIO.HIGH)
        # Allow it to get there.
        sleep(.005) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP_AZ,GPIO.LOW)
        sleep(.005) # Dictates how fast stepper motor will run

    GPIO.output(DIR_AZ, CW)
    GPIO.output(DIR_ALT, CW)
    return 0, offset


try:
    calibrate(0)


# Once finished clean everything up
except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()



