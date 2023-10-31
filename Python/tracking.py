"""
File: tracking.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Tracking methods for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""

import time
import RPi.GPIO as GPIO
from astropy.time import Time
from astropy.coordinates import get_sun, AltAz, EarthLocation
from utilities import Log

DIR_AZ = 10 # Azimuth stepper motor direction pin from controller
STEP_AZ = 8 # Azimuth stepper motor pin from controller
DIR_ALT = 13 # Altitude stepper motor direction pin from controller
STEP_ALT = 15 # Altitude stepper motor direction pin from controller
LIM_ALT = 7 # Limit switch 1 input from Pi
LIM_AZ = 11 # Limit switch 2 input from Pi
STEP_SIZE = 1.8 # Nema 23 Stepper Motor (1.8 step angle, 200 steps per revolutions)
CALIBRATION_ROTATION_SIZE = 1 # Number of degrees to move each step during calibration
CW = 1 # 0/1 used to signify clockwise or counterclockwise.
CCW = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(DIR_AZ, GPIO.OUT) # Establish Pins in software
GPIO.setup(STEP_AZ, GPIO.OUT)
GPIO.setup(DIR_ALT, GPIO.OUT)
GPIO.setup(STEP_ALT, GPIO.OUT)
GPIO.setup(LIM_ALT, GPIO.IN)
GPIO.setup(LIM_AZ, GPIO.IN)
GPIO.output(DIR_AZ, CCW) # Direction of calibration spin for azimuth stepper motor
GPIO.output(DIR_ALT, CCW) # Direction of calibration spin for altitude stepper motor

def calibrate(offset):
    """
    Calibrate the stepper motor to the limit switch and return the starting altitude and azimuth.

    :param offset: Azimuth offset in degrees.
    :return: Starting altitude and azimuth of the antenna in degrees. (0,0)
    """
    Log.info("Starting Calibration...")
    # Altitude calibration
    while(GPIO.input(LIM_ALT) != GPIO.HIGH):
        moveStepper(CALIBRATION_ROTATION_SIZE, 0)

    # Azimuth calibration
    while(GPIO.input(LIM_AZ) != GPIO.HIGH):
        moveStepper(0, CALIBRATION_ROTATION_SIZE)

    GPIO.output(DIR_AZ, CW)
    GPIO.output(DIR_ALT, CW)
    Log.info("Done Calibration.")
    return 0, offset

def getSunPosition(lat, lon):
    """
    Get the altitude and azimuth of the sun relative to the measurement location.

    :param lat: Latitude of the measurement location. (string)
    :param lon: Longitude of the measurement location. (string)
    :param current_time: Current time.
    :return: Relative sun altitude and azimuth in degrees. (float)
    """
    Log.info("Starting getSunPosition...")
    current_time = Time(time.time(), format='unix')
    current_time.format= "iso"
    sunPos = get_sun(current_time) # coordinates of the sun in GCRS frame
    measurementLoc = EarthLocation(lat = lat, lon = lon) # location of measurement
    relSunPos = sunPos.transform_to(AltAz(obstime = current_time, location = measurementLoc)) # sun position relative to measurement location

    Log.info("Time: " + str(current_time) + " Sun Alt: " + str(relSunPos.alt.deg) + " Sun Az: " + str(relSunPos.az.deg))
    Log.info("Done getSunPosition.")

    return relSunPos.alt.deg, relSunPos.az.deg
    
def getDifferenceDeg(antAlt, antAz, sunAlt, sunAz):
    """
    Calculate the difference in degrees between the antenna and the sun.

    :param antAlt: Current altitude of the antenna in degrees. (float)
    :param antAz: Current azimuth of the antenna in degrees. (float)
    :param sunAlt: Current altitude of the sun in degrees. (float)
    :param sunAz: Current azimuth of the sun in degrees. (float)
    :return: Difference in altitude and azimuth between antenna and sun in degrees. (float)
    """
    Log.info("Starting getDifferenceDeg...")

    diffAlt = sunAlt - antAlt
    diffAz = sunAz - antAz

    Log.info("Degrees to move in altitude: " + diffAlt + " Degrees to move in azimuth: " + diffAz)
    Log.info("Done getDifferenceDeg.")

    return diffAlt, diffAz

def moveStepper(diffAlt, diffAz):
    """
    Move the stepper motor based on the difference in altitude and azimuth.

    :param diffAlt: Difference in altitude between antenna and sun in degrees.
    :param diffAz: Difference in azimuth between antenna and sun in degrees.
    :return: None
    """
    Log.info("Starting moveStepper")

    # Number of steps required for difference in angles.
    stepsAlt = int(diffAlt / STEP_SIZE)
    stepsAz = int(diffAz / STEP_SIZE)

    # Function to rotate stepper motor.
    def rotateMotor(pin, steps):
        for _ in range(steps):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.001)  # TODO: Adjust sleep time.
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.001)  # TODO: Adjust sleep time.

    # Rotate the stepper motor for altitude and azimuth.
    rotateMotor(STEP_ALT, stepsAlt)
    rotateMotor(STEP_AZ, stepsAz)

    Log.info("Stepper motor moved. Altitude change: " + str(diffAlt) + " degrees, Azimuth change: " + str(diffAz) + " degrees")
    Log.info("Done moveStepper")
    return
