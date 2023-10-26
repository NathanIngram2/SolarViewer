"""
File: main.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Main program for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""

# Package imports
from astropy.time import Time
import argparse

# Method imports
from dataCollection import measPower, writeData, plotPower
from tracking import calibrate, getSunPosition, getDifferenceDeg, moveStepper
from utilities import Log

parser = argparse.ArgumentParser(
    description='Solar Viewer is designed to measure microwave radiation from the sun. This'
                ' program controls tracking the sun, collecting data, and data analysis.')

parser.add_argument('stop_time', type=str, help='Time to stop collecting data. Format HH:MM')
parser.add_argument('meas_interval', type=int, help='Time in minutes between measurements')
parser.add_argument('--azimuth_offset', type=int, nargs='?', const=0, default=0,
                    help='Specify primary lobes offset from horizontal in degrees (0 for horn, ~20 for dish). '
                         'Default = 0')
parser.add_argument('--integration_interval', type=str, nargs='?', const='1s', default='1s',
                    help='Integration integral of SDR power measurement. Ex. 1s, 1m, etc. Default = 1s')
parser.add_argument('--freq_min', type=str, nargs='?', const='980M', default='980M',
                    help='Start frequency for power measurement. Ex. 980M, 1G. Default = 980M')
parser.add_argument('--freq_max', type=str, nargs='?', const='1020M', default='1020M',
                    help='Stop frequency for power measurement. Ex. 980M, 1G. Default = 1020M')
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
LAT = args.latitude
LON = args.longitude
ANT_OFFSET_AZ = args.azimuth_offset
STOP_TIME = args.stop_time
MEAS_INTERVAL = args.meas_interval
FREQ_MIN = args.freq_min
FREQ_MAX = args.freq_max
INTEGRATION_INTERVAL = args.integration_interval

antAlt, antAz = calibrate(ANT_OFFSET_AZ)

timeData = []
powerData = []

current_time = Time.now()

while current_time < STOP_TIME:
    current_time = Time.now()
    sunAlt, sunAz = getSunPosition(LAT, LON, current_time)
    diffAlt, diffAz = getDifferenceDeg(antAlt, antAz, sunAlt, sunAz)
    moveStepper(diffAlt, diffAz)
    power = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL)
    writeData(current_time, power, sunAlt, sunAz)
    timeData.append(current_time)
    powerData.append(power)
    plotPower(timeData, powerData)

    wait(MEAS_INTERVAL)

# Save plot

calibrate(ANT_OFFSET_AZ)  # Return to zero position.
