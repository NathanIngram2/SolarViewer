"""
File: dataCollection.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Data collection and processing methods for the Solar Eclipse Viewer project
for ENPH454 @ Queen's University, Kingston ON.
"""

from utilities import Log

# collect measurement from SDR
# Return: power (dB)
def measPower(freq_min, freq_max, integration_interval):
    Log.info("Starting measPower with min: " + freq_min + " max: " + freq_max + " integration interval: "
             + integration_interval)

    Log.info("End measPower")
    return

def writeData(current_time, power, sunAlt, sunAz):
    Log.info("Starting writeData")
    Log.info("Writing " + current_time + " " + power + " " + sunAlt + " " + sunAz)

    Log.info("Done writeData")
    return

def plotPower(timeData, powerData):

    return