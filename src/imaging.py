"""
File: imaging.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Data collection and processing methods for the Solar Eclipse Viewer project
for ENPH454 @ Queen's University, Kingston ON.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import os

from dataCollection import measPower
from tracking import calibrate, getSunPosition, getDifferenceDeg, moveStepper
from utilities import Log

# TODO: Move to its own folder, image.py should have its own main.

# TODO: Implement a script to take an image by sweeping over a input range of Al and Az angles,
#  plot measurement as a heatmap (Az on x, Al on y).

parser = argparse.ArgumentParser(
    description='Solar Viewer is designed to measure microwave radiation from the sun. This'
                ' program controls tracking the sun, collecting data, and data analysis.')

parser.add_argument('--elevation_offset', type=float, nargs='?', const=0, default=0,
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
parser.add_argument('--img_start_alt', type=float, nargs='?', const=400, default=400,
                    help='Starting altitude of the sun, manual input for testing. Ex. 22.5. Default = 400')
parser.add_argument('--img_start_az', type=float, nargs='?', const=400, default=400,
                    help='Starting azimuth of the sun, manual input for testing. Ex. 22.5. Default = 400')
parser.add_argument('--verbose', type=str, choices={"LOW", "MED", "HIGH"}, nargs='?', const="HIGH",
                    default="HIGH", help="Select verbosity level of console output. Default = HIGH")
args = parser.parse_args()

# Setup Logging
log = Log(args, os.path.realpath(__file__))

# Constants and parsed arguments.
DISH_ARM_ANGLE_CALIBRATION = 62.5
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
IMG_START_ALT = args.img_start_alt
IMG_START_AZ = args.img_start_az

LOWER_LIM_ALT = 0
UPPER_LIM_ALT = 32
LOWER_LIM_AZ = 0
UPPER_LIM_AZ = 145

# Calibration and position determination
antAlt, antAz = calibrate(ANT_OFFSET_EL, ANT_OFFSET_AZ)
sunAlt, sunAz = getSunPosition(LAT, LON)

# If image start altitude and azimuth is specified, use that instead (testing)
# Otherwise calculate the starting Altitude and Azimuth based on the sun's position and image dimensions
if IMG_START_ALT != 400:
    startingAlt = IMG_START_ALT
else:
    startingAlt = sunAlt - (IMG_HEIGHT / 2)

if IMG_START_AZ != 400:
    startingAz = IMG_START_AZ
else:
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

# Save the collected data to a CSV file with a timestamp
np.savetxt(os.path.join(Log.logDirPath, "ImageData" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv"),
           data, delimiter=",")

# Display the collected data as an image
plt.imshow(data, origin='lower', interpolation=None)
plt.savefig(os.path.join(Log.logDirPath, "figure.png"))
plt.show()
