"""
File: dynamic_update_plot_test.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-11-25
Description: Dynamic plot test for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.

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

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import time

# Create figure for plotting
fig = plt.figure()
plt.ion()
plt.show()

def plot_live(x, y):
        plt.clf()
        plt.xlabel('Time')
        plt.ylabel('Power (dB)')
        plt.ylim(0,10)
        plt.plot(x, y, 'b.')
        plt.draw()

x = np.linspace(0,1,10)
y = x*10
xTest = []
yTest = []

for i in range(0, len(x)):
    xTest.append(x[i])
    yTest.append(y[i])
    plot_live(xTest, yTest)
    plt.pause(1)

plt.ioff()
plt.show()