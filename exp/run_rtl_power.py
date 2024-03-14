"""
File: run_rtl_power.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-11-25
Description: Test of rtl_power for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.

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

from solar_viewer_utilities import info, warn, error

while 1:
    info("Starting rtl_power")
    rst = sp.run(["rtl_power -f 980M:1020M:128k -g 0 -i 1s -1 tmp/rtl_power_out.csv"], shell=True, capture_output=True, text=True)
    info("Done rtl_power")
    raw = pd.read_csv("tmp/rtl_power_out.csv")
    proc = raw.iloc[:, 0:4]
    proc[len(proc.columns)] = raw.iloc[:, 6:-1].mean(axis=1)
    mean_all_freq_and_time = proc.iloc[:, 4].mean()

    warn("Power: " + str(mean_all_freq_and_time))

info("Exiting...")
