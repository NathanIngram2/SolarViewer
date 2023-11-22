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

DIR_AZ = 10  # Azimuth stepper motor direction pin from controller
STEP_AZ = 8  # Azimuth stepper motor pin from controller
DIR_ALT = 13  # Altitude stepper motor direction pin from controller
STEP_ALT = 15  # Altitude stepper motor direction pin from controller
LIM_ALT = 18  # Limit switch 1 input from Pi
LIM_AZ = 22  # Limit switch 2 input from Pi
STEP_SIZE = 0.45  # Nema 23 Stepper Motor (1.8 step angle, 200 steps per revolutions)
# TODO: Set CALIBRATION_ROTATION_SIZE appropriately
CALIBRATION_ROTATION_SIZE = 2  # Number of degrees to move each step during calibration
CW = 1  # 0/1 used to signify clockwise or counterclockwise.
CCW = 0

LOWER_LIM_ALT = 0
UPPER_LIM_ALT = 80
LOWER_LIM_AZ = 0
UPPER_LIM_AZ = 180

EL_GEAR_RATIO = 10
AZ_GEAR_RATIO = 4.4

# Set GPIO pin modes
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DIR_AZ, GPIO.OUT)
GPIO.setup(STEP_AZ, GPIO.OUT)
GPIO.setup(DIR_ALT, GPIO.OUT)
GPIO.setup(STEP_ALT, GPIO.OUT)
GPIO.setup(LIM_ALT, GPIO.IN)
GPIO.setup(LIM_AZ, GPIO.IN)
GPIO.output(DIR_AZ, CCW)  # Direction of calibration spin for azimuth stepper motor
GPIO.output(DIR_ALT, CCW)  # Direction of calibration spin for altitude stepper motor


def calibrate(offset):
    """
    Calibrate the stepper motor to the limit switch and return the starting altitude and azimuth.

    :param offset: Azimuth offset in degrees.
    :return: Starting altitude and azimuth of the antenna in degrees. (0,0)
    """
    Log.info("Starting Calibration...")
    # Altitude calibration
    while GPIO.input(LIM_ALT) != GPIO.HIGH:
        moveStepper(CALIBRATION_ROTATION_SIZE, 0)

    # Azimuth calibration
    while GPIO.input(LIM_AZ) != GPIO.HIGH:
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
    :return: Relative sun altitude and azimuth in degrees. (float)
    """
    Log.info("Starting getSunPosition...")
    current_time = Time(time.time(), format='unix')
    current_time.format = "iso"
    sunPos = get_sun(current_time)  # coordinates of the sun in GCRS frame
    measurementLoc = EarthLocation(lat=lat, lon=lon)  # location of measurement
    relSunPos = sunPos.transform_to(
        AltAz(obstime=current_time, location=measurementLoc))  # sun position relative to measurement location

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
    if sunAlt >= LOWER_LIM_ALT:
        if sunAlt <= UPPER_LIM_ALT:
            diffAlt = sunAlt - antAlt
        else:
            diffAlt = UPPER_LIM_ALT - antAlt
            Log.info("Sun Alt = " + str(sunAlt) + " greater than Altitude Upper Limit = " + str(
                UPPER_LIM_ALT) + ", moving to upper limit")
    else:
        diffAlt = antAlt - LOWER_LIM_ALT
        Log.info("Sun Alt = " + str(sunAlt) + " lower than Altitude Lower Limit = " + str(
            LOWER_LIM_ALT) + ", moving to lower limit")

    if sunAz >= LOWER_LIM_AZ:
        if sunAz <= UPPER_LIM_AZ:
            diffAz = sunAz - antAz
        else:
            diffAz = UPPER_LIM_AZ - antAz
            Log.info("Sun Az = " + str(sunAz) + " greater than Azimuth Upper Limit = " + str(
                UPPER_LIM_AZ) + ", moving to upper limit")
    else:
        diffAz = antAz - LOWER_LIM_AZ
        Log.info("Sun Az = " + str(sunAz) + " lower than Azimuth Lower Limit = " + str(
            LOWER_LIM_AZ) + ", moving to lower limit")

    Log.info("Degrees to move in altitude: " + str(diffAlt) + " Degrees to move in azimuth: " + str(diffAz))
    Log.info("Done getDifferenceDeg.")

    updatedAntAlt = antAlt + diffAlt
    updatedAntAz = antAz + diffAz

    return diffAlt, diffAz, updatedAntAlt, updatedAntAz


def moveStepper(diffAlt, diffAz):
    """
    Move the stepper motor based on the difference in altitude and azimuth.

    :param diffAlt: Difference in altitude between antenna and sun in degrees.
    :param diffAz: Difference in azimuth between antenna and sun in degrees.
    :return: None
    """
    Log.info("Starting moveStepper")

    # Number of steps required for difference in angles.
    # TODO: Integer cast will cause inaccurate tracking. Need to fix.
    stepsAlt = int((diffAlt / STEP_SIZE) * EL_GEAR_RATIO)
    stepsAz = int((diffAz / STEP_SIZE) * AZ_GEAR_RATIO)

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

    Log.info("Stepper motor moved. Altitude change: " + str(diffAlt) + " degrees, Azimuth change: " + str(
        diffAz) + " degrees")
    Log.info("Done moveStepper")
    return
