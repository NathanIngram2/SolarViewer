"""
File: tracking.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Tracking methods for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""

# Move stepper motor to limit switch in both axis, return the altitude and azmuth (0,0)
# Return: alt, az + offset
def calibrate(offset):

    return
    
# Use astropy to calculate altitude and azmuth of sun
# Return: alt, az
def getSunPosition(lat, lon, current_time):

    return
    
# Calculates how many degrees the stepper motor needs to move in each axis
# Return: diffAlt, diffAz
def getDifferenceDeg(antAlt, antAz, sunAlt, sunAz):

    return

# Move stepper
# Return: null
def moveStepper(diffAlt, diffAz):

    return