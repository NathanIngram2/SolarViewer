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

parser = argparse.ArgumentParser(
    description='Solar Viewer is designed to measure microwave radiation from the sun. This'
                ' program controls tracking the sun, collecting data, and data analysis.')

parser.add_argument('stop_time', type=str, help='Time to stop collecting data. Format HH:MM')
parser.add_argument('meas_interval', type=int, help='Time in minutes between measurements')
parser.add_argument('--azimuth_offset', type=int, nargs='?', const=0, default=0,
                    help='Specify primary lobes offset from horizontal in degrees (0 for horn, ~20 for dish)')
parser.add_argument('--integration_interval', type=str, nargs='?', const='1s', default='1s',
                    help='Integration integral of SDR power measurement. Ex. 1s, 1m, etc.')
parser.add_argument('--freq_min', type=str, nargs='?', const='980M', default='980M',
                    help='Start frequency for power measurement. Ex. 980M, 1G')
parser.add_argument('--freq_max', type=str, nargs='?', const='1020M', default='1020M',
                    help='Stop frequency for power measurement. Ex. 980M, 1G')
parser.add_argument('--latitude', type=str, nargs='?', const='+44d13m29s', default='+44d13m29s',
                    help='Latitude of location')
parser.add_argument('--longitude', type=str, nargs='?', const='-76d29m52s', default='-76d29m52s',
                    help='Longitude of location')
args = parser.parse_args()

# Constants and parsed arguments.
LAT = args.latitude
LON = args.longitude
ANT_OFFSET_AZ = args.azimuth_offset
STOP_TIME = args.stop_time
MEAS_INTERVAL = args.meas_interval
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
    power = measPower(INTEGRATION_INTERVAL)
    writeData(current_time, power, sunAlt, sunAz)
    timeData.append(current_time)
    powerData.append(power)
    plotPower(timeData, powerData)

    wait(MEAS_INTERVAL)

# Save plot

calibrate(ANT_OFFSET_AZ)  # Return to zero position.
