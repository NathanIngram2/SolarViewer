"""
File: tracking.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Tracking methods for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.


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
CW = 1  # 0/1 used to signify clockwise or counterclockwise.
CCW = 0

LOWER_LIM_ALT = 0
UPPER_LIM_ALT = 32
LOWER_LIM_AZ = 0
UPPER_LIM_AZ = 145

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


def calibrate(offsetAlt, offsetAz):
    """
    Calibrate the stepper motor to the limit switch and return the starting altitude and azimuth.

    :param offsetAlt: Altitude offset in degrees.
    :param offsetAz: Azimuth offset in degrees.
    :return: Starting altitude and azimuth of the antenna in degrees. (0,0)
    """
    Log.info("Starting Calibration...")

    alt_step = -0.05
    az_step = -0.12

    total_alt = 0
    total_az = 0

    # Altitude calibration
    while GPIO.input(LIM_ALT) != GPIO.HIGH:
        moveStepper(alt_step, 0, cal_flag=True)
        time.sleep(0.001)
        total_alt += alt_step
    # Azimuth calibration
    while GPIO.input(LIM_AZ) != GPIO.HIGH:
        moveStepper(0, az_step, cal_flag=True)
        time.sleep(0.001)
        total_az += az_step

    Log.info(f"Done Calibration. Moved {total_alt} deg in altitude, {total_az} deg in azimuth.")
    return offsetAlt, offsetAz


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


def getDifferenceDeg(antAlt, antAz, sunAlt, sunAz, offsetAlt, offsetAz):
    """
    Calculate the difference in degrees between the antenna and the sun.

    :param antAlt: Current altitude of the antenna in degrees. (float)
    :param antAz: Current azimuth of the antenna in degrees. (float)
    :param sunAlt: Current altitude of the sun in degrees. (float)
    :param sunAz: Current azimuth of the sun in degrees. (float)
    :param offsetAlt: Offset altitude of the antenna in degrees. (float)
    :param offsetAz: Offset azimuth of the antenna in degrees. (float)
    :return: Difference in altitude and azimuth between antenna and sun in degrees. (float)
    """
    #Log.info("Starting getDifferenceDeg...")
    if sunAlt >= (LOWER_LIM_ALT + offsetAlt):
        if sunAlt <= (UPPER_LIM_ALT + offsetAlt):
            diffAlt = sunAlt - antAlt
        else:
            diffAlt = (UPPER_LIM_ALT + offsetAlt) - antAlt
            Log.info("Sun Alt = " + str(sunAlt) + " greater than Altitude Upper Limit = " + str(
                UPPER_LIM_ALT + offsetAlt) + ", moving to upper limit")
    else:
        diffAlt = antAlt - (LOWER_LIM_ALT + offsetAlt)
        Log.info("Sun Alt = " + str(sunAlt) + " lower than Altitude Lower Limit = " + str(
            LOWER_LIM_ALT + offsetAlt) + ", moving to lower limit")

    if sunAz >= (LOWER_LIM_AZ + offsetAz):
        if sunAz <= (UPPER_LIM_AZ + offsetAz):
            diffAz = sunAz - antAz
        else:
            diffAz = (UPPER_LIM_AZ + offsetAz) - antAz
            Log.info("Sun Az = " + str(sunAz) + " greater than Azimuth Upper Limit = " + str(
                UPPER_LIM_AZ + offsetAz) + ", moving to upper limit")
    else:
        diffAz = antAz - (LOWER_LIM_AZ + offsetAz)
        Log.info("Sun Az = " + str(sunAz) + " lower than Azimuth Lower Limit = " + str(
            LOWER_LIM_AZ + offsetAz) + ", moving to lower limit")

    Log.info("Degrees to move in altitude: " + str(diffAlt) + " Degrees to move in azimuth: " + str(diffAz))
    #Log.info("Done getDifferenceDeg.")

    updatedAntAlt = antAlt + diffAlt
    updatedAntAz = antAz + diffAz

    return diffAlt, diffAz, updatedAntAlt, updatedAntAz


def moveStepper(diffAlt, diffAz, cal_flag=False):
    """"""
    """
    Move the stepper motor based on the difference in altitude and azimuth.

    :param diffAlt: Difference in altitude between antenna and sun in degrees.
    :param diffAz: Difference in azimuth between antenna and sun in degrees.
    :param cal_flag: Flag to indicate if moveStepper is being called from calibration. Does not log if True
    :return: None
    """
    #Log.info("Starting moveStepper")

    if diffAz < 0:
        GPIO.output(DIR_AZ, CW)
    else:
        GPIO.output(DIR_AZ, CCW)

    if diffAlt < 0:
        GPIO.output(DIR_ALT, CCW)
    else:
        GPIO.output(DIR_ALT, CW)

    # Number of steps required for difference in angles.
    stepsAlt = (diffAlt / STEP_SIZE) * EL_GEAR_RATIO
    stepsAz = (diffAz / STEP_SIZE) * AZ_GEAR_RATIO

    stepsAltInt = abs(int(stepsAlt))
    stepsAzInt = abs(int(stepsAz))

    # Function to rotate stepper motor.
    def rotateMotor(pin, steps):
        for _ in range(steps):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.001)  # TODO: Adjust sleep time.
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.05)  # TODO: Adjust sleep time.

    # Rotate the stepper motor for altitude and azimuth.
    rotateMotor(STEP_ALT, stepsAltInt)
    rotateMotor(STEP_AZ, stepsAzInt)

    degErrorAlt = stepsAltInt - stepsAlt
    degErrorAz = stepsAzInt - stepsAz

    if not cal_flag:
        Log.info("Stepper motor moved, Altitude change: " + str(diffAlt) + " degrees, Azimuth change: " + str(
            diffAz) + " degrees")
    #Log.info("Done moveStepper")

    return degErrorAlt, degErrorAz

def positionErrorCorrection(antAlt, antAz, degErrorAlt, degErrorAz):
    Log.info("Starting positionErrorCorrection")

    Log.info("Correcting elevation by: " + str(degErrorAlt) + " deg")
    Log.info("Correcting azimuth by: " + str(degErrorAz) + " deg")
    correctedAntAlt = antAlt + degErrorAlt
    correctedAntAz = antAz + degErrorAz

    Log.info("Done positionErrorCorrection")
    return correctedAntAlt, correctedAntAz
