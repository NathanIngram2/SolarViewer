"""
File: tracking.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Tracking methods for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""

import astropy.coordinates as coordinates
from utilities import Log
from astropy.coordinates import get_sun, AltAz, EarthLocation

# Move stepper motor to limit switch in both axis, return the altitude and azimuth (0,0)
# Return: alt, az + offset (float) = starting altitude and azimuth of antenna in degrees
def calibrate(offset):
    Log.info("Starting Calibration...")

    Log.info("Done Calibration.")
    return
    
# Use astropy to calculate altitude and azmuth of sun
# Params: lat (string) = latitude of measurement location in the form '+44d13m29s'
#         lon (string) = longitude of measurement location in the form '-76d29m52s'
# Return: alt, az (float) = relative sun altitude and azimuth in degrees
def getSunPosition(lat, lon, current_time):
    Log.info("Starting getSunPosition...")

    sunPos = get_sun(current_time) # coordinates of the sun in GCRS frame
    measurementLoc = coordinates.EarthLocation(lat = lat, lon = lon) # location of measurement
    relSunPos = sunPos.transform_to(AltAz(obstime = current_time, location = measurementLoc)) # sun position relative to measurement location

    Log.info("Time: " + current_time + " Sun Alt: " + relSunPos.alt.deg + " Sun Az: " + relSunPos.az.deg)
    Log.info("Done getSunPosition.")

    return relSunPos.alt.deg, relSunPos.az.deg
    
# Calculates how many degrees the stepper motor needs to move in each axis
# Params: antAlt (float) = current altitude of the antenna in degrees
#         antAz (float) = current azimuth of the antenna in degrees
#         sunAlt (float) = current altitude of the sun in degrees
#         sunAz (float) = current azimuth of the sun in degrees
# Return: diffAlt, diffAz (float) = difference in altitude and azimuth between antenna and sun in degrees
def getDifferenceDeg(antAlt, antAz, sunAlt, sunAz):
    Log.info("Starting getDifferenceDeg...")

    diffAlt = sunAlt - antAlt
    diffAz = sunAz - antAz

    Log.info("Degrees to move in altitude: " + diffAlt + " Degrees to move in azimuth: " + diffAz)
    Log.info("Done getDifferenceDeg.")

    return diffAlt, diffAz

# Move stepper
# Return: null
def moveStepper(diffAlt, diffAz):
    Log.info("Starting moveStepper...")

    Log.info("Done moveStepper...")
    return