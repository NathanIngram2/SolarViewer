"""
File: parse_args.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-11-25
Description: Arg parsing test for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.

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

import argparse
# Command line argument parser.
parser = argparse.ArgumentParser(
    description='Solar Viewer is designed to measure microwave radiation from the sun. This'
                ' program controls tracking the sun, collecting data, and data analysis.')
parser.add_argument('stop_time', type=str, help='Time to stop collecting data. Format HH:MM')
parser.add_argument('meas_interval', type=int, help='Time in minutes between measurements')

parser.add_argument('--azimuth_offset', type=int, nargs='?', const=0, default=0, help='Specify primary lobes offset from horizontal in degrees (0 for horn, ~20 for dish)')

parser.add_argument('--integration_interval', type=str, nargs='?', const='1s', default='1s', help='Integration integral of SDR power measurement. Ex. 1s, 1m, etc.')
parser.add_argument('--freq_min', type=str, nargs='?', const='980M', default='980M', help='Start frequency for power measurement. Ex. 980M, 1G')
parser.add_argument('--freq_max', type=str, nargs='?', const='1020M', default='1020M', help='Stop frequency for power measurement. Ex. 980M, 1G')

parser.add_argument('--latitude', type=str, nargs='?', const='+44d13m29s', default='+44d13m29s', help='Latitude of location')
parser.add_argument('--longitude', type=str, nargs='?', const='-76d29m52s', default='-76d29m52s', help='Longitude of location')

args = parser.parse_args()
print(args)