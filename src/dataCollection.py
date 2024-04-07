"""
File: dataCollection.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Data collection and processing methods for the Solar Eclipse Viewer project
for ENPH454 @ Queen's University, Kingston ON.


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

import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt
import os
from utilities import Log


def measPower(freq_min, freq_max, integration_interval, gain):
    """
    Measure the power using rtl_power and return the mean power over all frequencies and time.

    :param freq_min: Minimum frequency for power measurement.
    :param freq_max: Maximum frequency for power measurement.
    :param integration_interval: Integration interval for SDR power measurement.
    :param gain: Input gain for RTL-SDR
    :return: Mean power (dB) over all frequencies and time.
    """
    Log.info("Starting measPower with min: " + str(freq_min) + " max: " + str(freq_max) + " integration interval: "
             + integration_interval)

    command = ('rtl_power -f ' + str(freq_min) + ':' + str(freq_max) + ':128k -i ' + str(integration_interval)
               + ' -g ' + str(gain) + ' -1 tmp/rtl_power_out.csv')
    Log.info("Executing command: " + str(command))

    # TODO: Parse rst for error message or nan. Log error.
    try:
        #rst = sp.run([command], shell=True, capture_output=True, text=True, check=True) # TODO: check=True was causing issues in testing
        rst = sp.run([command], shell=True, capture_output=True, text=True, timeout=4)
    except:
        Log.error("Error executing rtl_power command")
        Log.error("User must manually reset SDR now")
        input("Press enter once SDR reset...")
        try:
            Log.info("2nd attempt executing command: " + str(command))
            rst = sp.run([command], shell=True, capture_output=True, text=True, timeout=4)
        except:
            Log.error("Error occurred again. Exiting program.")
            exit()
        #sp.run(['./resetusb'], shell=True, capture_output=True, text=True, timeout=1)

    Log.info("Done rtl_power. Reading CSV...")
    raw = pd.read_csv("tmp/rtl_power_out.csv")
    proc = raw.iloc[:, 0:4]
    proc[len(proc.columns)] = raw.iloc[:, 6:-1].mean(axis=1)
    mean_all_freq_and_time = proc.iloc[:, 4].mean()

    Log.info("Power: " + str(mean_all_freq_and_time))
    Log.info("End measPower")

    return mean_all_freq_and_time


def writeData(current_time, power, sunAlt, sunAz):
    """
    Write data to a CSV file.

    :param current_time: Current time of the measurement.
    :param power: Power measurement.
    :param sunAlt: Sun's altitude.
    :param sunAz: Sun's azimuth.
    :return: None
    """
    Log.info("Starting writeData")
    Log.info("Writing " + str(current_time) + " " + str(power) + " " + str(sunAlt) + " " + str(sunAz))

    data = pd.DataFrame({
        'Time': [current_time],
        'Power': [power],
        'SunAltitude': [sunAlt],
        'SunAzimuth': [sunAz]
    })

    try:
        data.to_csv('data.csv', mode='a', header=False, index=False)
    except IOError as e:
        Log.error("Error writing to data.csv: " + str(e))
        return

    Log.info("End writeData")


def plotPower(timeData, powerData, savePlot=False):
    """
    Plot power as a function of time.

    :param timeData: List of time data.
    :param powerData: List of power data.
    :return: None
    """
    Log.info("Starting plotPower")

    plt.clf()
    plt.xlabel('Time')
    plt.ylabel('Power (dB)')
    plt.title('Power vs Time')
    plt.ylim(-35,-30)
    plt.plot(timeData, powerData, 'b.')
    plt.draw()

    if savePlot == True:
        plt.savefig(os.path.join(Log.logDirPath, 'plot.png'))

    Log.info("End plotPower")
    return


