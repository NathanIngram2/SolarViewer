"""
File: main.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Main program for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""

# Package imports
import argparse
import time
import datetime
import matplotlib.pyplot as plt

# Method imports
from dataCollection import measPower, writeData, plotPower
from tracking import calibrate, getSunPosition, getDifferenceDeg, moveStepper, positionErrorCorrection
from utilities import Log

parser = argparse.ArgumentParser(
    description='Solar Viewer is designed to measure microwave radiation from the sun. This'
                ' program controls tracking the sun, collecting data, and data analysis.')

parser.add_argument('duration', type=str,
                    help='Duration of elapsed time taking data. Format HH:MM - HH(00-23):MM(00-59)')
parser.add_argument('meas_interval', type=str,
                    help='Time in minutes between measurements. Format MM(0-59)')
parser.add_argument('--elevation_offset', type=float, nargs='?', const=0, default=0,
                    help='Specify primary lobes offset from horizontal in degrees (0 for horn, ~20 for dish). Default = 0')
parser.add_argument('--azimuth_offset', type=float, nargs='?', const=0, default=0,
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
parser.add_argument('--verbose', type=str, choices={"LOW", "MED", "HIGH"}, nargs='?', const="HIGH",
                    default="HIGH", help="Select verbosity level of console output. Default = HIGH")
args = parser.parse_args()

# Setup Logging
log = Log(args.verbose)

# Constants and parsed arguments.
DISH_ARM_ANGLE_CALIBRATION = 62.5
LAT = args.latitude
LON = args.longitude
ANT_OFFSET_EL = args.elevation_offset
ANT_OFFSET_AZ = args.azimuth_offset + DISH_ARM_ANGLE_CALIBRATION
FREQ_MIN = args.freq_min
FREQ_MAX = args.freq_max
INTEGRATION_INTERVAL = args.integration_interval
DUR = args.duration
GAIN = args.gain


duration_hrs = int(DUR.split(":")[0])
duration_mins = int(DUR.split(":")[1])
current_time = datetime.datetime.now(tz=None)
duration_hrs_min = datetime.timedelta(hours=duration_hrs, minutes=duration_mins)
end_time = current_time + duration_hrs_min

meas_interval = int(float(args.meas_interval) * 60)

timeData = []
powerData = []

# Create figure for plotting
fig = plt.figure()
plt.ion()

# Calibrate mechanical setup
antAlt, antAz = calibrate(ANT_OFFSET_EL, ANT_OFFSET_AZ)

while current_time < end_time:
    sunAlt, sunAz = getSunPosition(LAT, LON)
    diffAlt, diffAz, antAlt, antAz = getDifferenceDeg(antAlt, antAz, sunAlt, sunAz,  ANT_OFFSET_EL, ANT_OFFSET_AZ)
    degErrorAlt, degErrorAz = moveStepper(diffAlt, diffAz)
    antAlt, antAz = positionErrorCorrection(antAlt, antAz, degErrorAlt, degErrorAz)
    power = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL, GAIN)
    current_time = datetime.datetime.now(tz=None)
    writeData(current_time, power, sunAlt, sunAz)
    timeData.append(current_time)
    powerData.append(power)
    plotPower(timeData, powerData)
    plt.pause(meas_interval)

# TODO: Add save plot
plt.ioff()
plt.show()

# Save plot
plotPower(timeData, powerData, savePlot=True)

calibrate(ANT_OFFSET_EL)  # Return Al and Az rotators to zero position.
