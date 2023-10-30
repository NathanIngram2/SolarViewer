"""
File: tracking.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Tracking methods for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""

import time
import pigpio as GPIO
from astropy.coordinates import get_sun, AltAz, EarthLocation
from utilities import Log

DIR = 10 # Direction pin from controller
STEP = 8 # Step pin from controller
STEP_SIZE = 1.8 # Nema 23 Stepper Motor (1.8 step angle, 200 steps per revolutions)
CW = 1 # 0/1 used to signify clockwise or counterclockwise.
CCW = 0

# Needs to be initalized before any other commands
pi = GPIO.pi()
if not pi.connected:
    exit()

#pi.set_mode(GPIO.BOARD) # Setup pin layout on PI
pi.set_mode(DIR, GPIO.OUT) # Establish Pins in software
pi.set_mode(STEP, GPIO.OUT)
pi.write(DIR, CW) # Direction of starting spin

def calibrate(offset):
    """
    Calibrate the stepper motor to the limit switch and return the starting altitude and azimuth.

    :param offset: Azimuth offset in degrees.
    :return: Starting altitude and azimuth of the antenna in degrees. (0,0)
    """
    Log.info("Starting Calibration...")

    Log.info("Done Calibration.")
    return

def getSunPosition(lat, lon, current_time):
    """
    Get the altitude and azimuth of the sun relative to the measurement location.

    :param lat: Latitude of the measurement location. (string)
    :param lon: Longitude of the measurement location. (string)
    :param current_time: Current time.
    :return: Relative sun altitude and azimuth in degrees. (float)
    """
    Log.info("Starting getSunPosition...")

    sunPos = get_sun(current_time) # coordinates of the sun in GCRS frame
    measurementLoc = EarthLocation(lat = lat, lon = lon) # location of measurement
    relSunPos = sunPos.transform_to(AltAz(obstime = current_time, location = measurementLoc)) # sun position relative to measurement location

    Log.info("Time: " + current_time + " Sun Alt: " + relSunPos.alt.deg + " Sun Az: " + relSunPos.az.deg)
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
            pi.write(pin, GPIO.HIGH)
            time.sleep(0.001)  # TODO: Adjust sleep time.
            pi.write(pin, GPIO.LOW)
            time.sleep(0.001)  # TODO: Adjust sleep time.

    # Rotate the stepper motor for altitude and azimuth.
    rotateMotor(STEP, stepsAlt)
    # TODO: Implement azimuthal control.
    # rotateMotor(STEP, diffAz)

    Log.info("Stepper motor moved. Altitude change: " + diffAlt + " degrees, Azimuth change: " + diffAz + " degrees")
    Log.info("Done moveStepper")
    return