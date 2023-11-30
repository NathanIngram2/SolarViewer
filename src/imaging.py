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

from dataCollection import measPower
from tracking import calibrate, getSunPosition, getDifferenceDeg, moveStepper
from utilities import Log

# TODO: Move to its own folder, image.py should have its own main.

# TODO: Implement a script to take an image by sweeping over a input range of Al and Az angles,
#  plot measurement as a heatmap (Az on x, Al on y).

parser = argparse.ArgumentParser(
    description='Solar Viewer is designed to measure microwave radiation from the sun. This'
                ' program controls tracking the sun, collecting data, and data analysis.')

parser.add_argument('--elevation_offset', type=int, nargs='?', const=0, default=0,
                    help='Specify primary lobes offset from horizontal in degrees (0 for horn, ~20 for dish). Default = 0')
parser.add_argument('--azimuth_offset', type=int, nargs='?', const=0, default=0,
                    help='Specify primary lobes offset from vertical in degrees. Default = 0')
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
parser.add_argument('--image_width', type=int, nargs='?', const=0, default=8,
                    help='Height of image in degrees (int). Default = 8')
parser.add_argument('--image_height', type=int, nargs='?', const=0, default=8,
                    help='Width of image in degrees (int). Default = 8')
args = parser.parse_args()

# Setup Logging
log = Log("HIGH")

DISH_ARM_ANGLE_CALIBRATION = 62.5

# Constants and parsed arguments.
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

antAlt, antAz = calibrate(ANT_OFFSET_EL, ANT_OFFSET_AZ)
sunAlt, sunAz = getSunPosition(LAT, LON)

startingAlt = sunAlt - (IMG_HEIGHT / 2)
finalAlt = sunAlt + (IMG_HEIGHT / 2)
startingAz = sunAz - (IMG_WIDTH / 2)
finalAz = sunAlt + (IMG_WIDTH / 2)

diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, startingAlt, startingAz, ANT_OFFSET_EL, ANT_OFFSET_AZ)
degErrorAlt, degErrorAz = moveStepper(diffAlt, diffAz)

data = np.zeros((ANT_OFFSET_EL, ANT_OFFSET_AZ))

for i in range(finalAlt):
    if i % 2 == 0:
        for j in range(finalAz):
            data[i][j] = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL, GAIN)
            diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, antAlt, antAz + 1, ANT_OFFSET_EL, ANT_OFFSET_AZ)
            moveStepper(0, diffAz)
            time.sleep(0.2)
    else:
        for j in range(finalAz):
            data[i][j] = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL, GAIN)
            diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, antAlt, antAz - 1, ANT_OFFSET_EL, ANT_OFFSET_AZ)
            moveStepper(0, diffAz)
            time.sleep(0.2)
    diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, antAlt + 1, antAz, ANT_OFFSET_EL, ANT_OFFSET_AZ)
    moveStepper(diffAlt, 0)

np.savetxt("ImageData" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv", data, delimiter=",")
plt.imshow(data, origin='lower', interpolation=None)
plt.show()
