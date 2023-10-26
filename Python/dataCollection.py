"""
File: dataCollection.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Data collection and processing methods for the Solar Eclipse Viewer project
for ENPH454 @ Queen's University, Kingston ON.
"""

import subprocess as sp
import pandas as pd

from utilities import Log

# collect measurement from SDR
# Return: power (dB)
def measPower(freq_min, freq_max, integration_interval):
    Log.info("Starting measPower with min: " + freq_min + " max: " + freq_max + " integration interval: "
             + integration_interval)

    command = ('rtl_power -f ' + freq_min + ':' + freq_max + ':128k -i ' + integration_interval
               + ' -1 tmp/rtl_power_out.csv')
    Log.info("Executing command: " + command)
    rst = sp.run([command], shell=True, capture_output=True,
                 text=True)
    # TODO: Parse rst for error message or nan. Log error.
    Log.info("Done rtl_power. Reading CSV...")
    raw = pd.read_csv("tmp/rtl_power_out.csv")
    proc = raw.iloc[:, 0:4]
    proc[len(proc.columns)] = raw.iloc[:, 6:-1].mean(axis=1)
    mean_all_freq_and_time = proc.iloc[:, 4].mean()

    Log.info("Power: " + str(mean_all_freq_and_time))
    Log.info("End measPower")

    return mean_all_freq_and_time

def writeData(current_time, power, sunAlt, sunAz):
    Log.info("Starting writeData")
    Log.info("Writing " + current_time + " " + power + " " + sunAlt + " " + sunAz)

    Log.info("Done writeData")
    return

def plotPower(timeData, powerData):

    return