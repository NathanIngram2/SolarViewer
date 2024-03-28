"""
File: eclipseImaging.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2024-03-22
Description: Main program for Imaging of the 2024 Solar Eclipse Viewer for Queen's University, Kingston ON.


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

# Package imports
import argparse
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import os

# Method imports
from dataCollection import measPower
from tracking import calibrate, getSunPosition, getDifferenceDeg, moveStepper
from utilities import Log

parser = argparse.ArgumentParser(
    description='Solar Viewer is designed to measure microwave radiation from the sun. This'
                ' program controls tracking the sun, collecting data, and data analysis.')

parser.add_argument('duration', type=str, nargs='?', const=3, default = 3
                    help='Duration of elapsed time taking data. Format HH - HH(00-23)')
parser.add_argument('meas_interval', type=str, nargs='?', const=5, default = 5
                    help='Time in minutes between measurements. Format MM(0-59)')
parser.add_argument('--elevation_offset', type=float, nargs='?', const=0, default=22.5,
                    help='Specify primary lobes offset from horizontal in degrees (0 for horn, ~20 for dish). Default = 0')
parser.add_argument('--azimuth_offset', type=float, nargs='?', const=0, default=0,
                    help='Specify primary lobes offset from north in degrees. Default = 0')
parser.add_argument('--integration_interval', type=str, nargs='?', const='1s', default='1s',
                    help='Integration integral of SDR power measurement. Ex. 1s, 1m, etc. Default = 1s')
parser.add_argument('--freq_min', type=str, nargs='?', const='980M', default='980M',
                    help='Start frequency for power measurement. Ex. 980M, 1G. Default = 980M')
parser.add_argument('--freq_max', type=str, nargs='?', const='1020M', default='1020M',
                    help='Stop frequency for power measurement. Ex. 980M, 1G. Default = 1020M')
parser.add_argument('--gain', type=str, nargs='?', const='0', default='0',
                    help='RTL-SDR input gain. Default = 0')
parser.add_argument('--latitude', type=str, nargs='?', const='+44d13m29s', default='+44d13m29s',
                    help='Latitude of location. Default = +44d13m29s')
parser.add_argument('--longitude', type=str, nargs='?', const='-76d29m52s', default='-76d29m52s',
                    help='Longitude of location. Default = -76d29m52s')
parser.add_argument('--image_width', type=int, nargs='?', const=8, default=8,
                    help='Height of image in degrees (int). Default = 8')
parser.add_argument('--image_height', type=int, nargs='?', const=8, default=8,
                    help='Width of image in degrees (int). Default = 8')
parser.add_argument('--verbose', type=str, choices={"LOW", "MED", "HIGH"}, nargs='?', const="HIGH",
                    default="HIGH", help="Select verbosity level of console output. Default = HIGH")
args = parser.parse_args()

# Setup Logging
log = Log(args, os.path.realpath(__file__))

# Constants and parsed arguments.
DISH_ARM_ANGLE_CALIBRATION = 47.5 # Updated March 28 after testing
LAT = args.latitude
LON = args.longitude
ANT_OFFSET_EL = args.elevation_offset
ANT_OFFSET_AZ = args.azimuth_offset + DISH_ARM_ANGLE_CALIBRATION
FREQ_MIN = args.freq_min
FREQ_MAX = args.freq_max
INTEGRATION_INTERVAL = args.integration_interval
GAIN = args.gain
IMG_WIDTH = args.image_width
IMG_HEIGHT = args.image_height
DUR = args.duration
MEAS_INTERVAL = args.meas_interval

LOWER_LIM_ALT = 0
UPPER_LIM_ALT = 32
LOWER_LIM_AZ = 0
UPPER_LIM_AZ = 145

ECLIPSE_START_TIME = datetime.datetime(2024,04,08,14,09,00) # Starts at 2:09pm
ECLIPSE_END_TIME = datetime.datetime(2024,04,08,16,35,00) # Starts at 2:09pm

duration_hrs = int(DUR.split(":")[0])
current_time = datetime.datetime.now(tz=None)
duration_hrs_min = datetime.timedelta(hours=duration_hrs)
end_time = current_time + duration_hrs_min

meas_interval = int(float(MEAS_INTERVAL) * 60)

# Calibration and position determination
antAlt, antAz = calibrate(ANT_OFFSET_EL, ANT_OFFSET_AZ)

while current_time < end_time:
    sunAlt, sunAz = getSunPosition(LAT, LON)

    # Calculate the starting Altitude and Azimuth based on the sun's position and image dimensions
    startingAlt = sunAlt - (IMG_HEIGHT / 2)
    startingAz = sunAz - (IMG_WIDTH / 2)
    finalAlt = startingAlt + IMG_HEIGHT
    finalAz = startingAz + IMG_WIDTH

    # Checking that entire image is within limits before beginning
    Log.info("Checking bounds of image are within limits...")
    if finalAlt > (UPPER_LIM_ALT + ANT_OFFSET_EL) or finalAlt < (LOWER_LIM_ALT + ANT_OFFSET_EL):
        Log.error("Image Final altitude - " + str(finalAlt) + " is out of range. Exiting")
        exit()
    if startingAlt > (UPPER_LIM_ALT + ANT_OFFSET_EL) or startingAlt < (LOWER_LIM_ALT + ANT_OFFSET_EL):
        Log.error("Image Starting altitude - " + str(startingAlt) + " is out of range. Exiting")
        exit()
    if finalAz > (UPPER_LIM_AZ + ANT_OFFSET_AZ) or finalAz < (LOWER_LIM_AZ + ANT_OFFSET_AZ):
        Log.error("Image Final azimuth - " + str(finalAz) + " is out of range. Exiting")
        exit()
    if startingAz > (UPPER_LIM_AZ + ANT_OFFSET_AZ) or startingAz < (LOWER_LIM_AZ + ANT_OFFSET_AZ):
        Log.error("Image Starting azimuth - " + str(startingAz) + " is out of range. Exiting")
        exit()
    Log.info("All image bounds are within limits.")

    data, antAlt, antAz = moveAndTakeImage(antAlt, antAz, startingAlt, startingAz)

    # Save the collected data to a CSV file with a timestamp
    np.savetxt(os.path.join(Log.logDirPath, "ImageData" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv"),
               data, delimiter=",")

    # Display the collected data as an image
    plt.imshow(data, origin='lower', interpolation=None)
    plt.savefig(os.path.join(Log.logDirPath, "figure.png"))
    plt.show()

    current_time = datetime.datetime.now(tz=None)

    if(ECLIPSE_START_TIME >= current_time or ECLIPSE_END_TIME <= current_time):
        plt.pause(meas_interval)


def moveAndTakeImage(antAlt, antAz, startingAlt, startingAz):
    # Initial calculation of the difference in degrees between antenna and starting position
    diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, startingAlt, startingAz, ANT_OFFSET_EL, ANT_OFFSET_AZ)
    degErrorAlt, degErrorAz = moveStepper(diffAlt, diffAz)

    # Initialize a 2D array to store the data collected
    data = np.zeros((IMG_HEIGHT, IMG_WIDTH))

    # Data collection loop, scanning over the specified range in Altitude and Azimuth
    for i in range(IMG_HEIGHT):
        # Alternate scanning direction for each row to improve efficiency
        if i % 2 == 0:
            for j in range(IMG_WIDTH):
                data[i][j] = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL, GAIN)
                diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, antAlt, antAz + 1, ANT_OFFSET_EL, ANT_OFFSET_AZ)
                moveStepper(0, diffAz)
                time.sleep(0.2)
        else:
            for j in range(IMG_WIDTH):
                data[i][IMG_WIDTH-j-1] = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL, GAIN)
                diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, antAlt, antAz - 1, ANT_OFFSET_EL, ANT_OFFSET_AZ)
                moveStepper(0, diffAz)
                time.sleep(0.2)
        diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, antAlt + 1, antAz, ANT_OFFSET_EL, ANT_OFFSET_AZ)
        moveStepper(diffAlt, 0)

    return data, antAlt, antAz

