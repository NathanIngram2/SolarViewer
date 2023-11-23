"""
File: imaging.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Data collection and processing methods for the Solar Eclipse Viewer project
for ENPH454 @ Queen's University, Kingston ON.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

from dataCollection import measPower
from tracking import calibrate, moveStepper
from utilities import Log

# TODO: Move to its own folder, image.py should have its own main.

# TODO: Implement a script to take an image by sweeping over a input range of Al and Az angles,
#  plot measurement as a heatmap (Az on x, Al on y).

# Setup Logging
log = Log("HIGH")

FREQ_MIN = "980M"
FREQ_MAX = "1020M"
INTEGRATION_INTERVAL = "1s"
GAIN = "0"
ANT_OFFSET_EL = 0

AZ_MAX = 120
EL_MAX = 60

calibrate(ANT_OFFSET_EL)

data = np.zeros((EL_MAX, AZ_MAX))

for i in range(EL_MAX):
    if i % 2 == 0:
        for j in range(AZ_MAX):
            data[i][j] = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL, GAIN)
            moveStepper(0, 1)
            time.sleep(0.2)
    else:
        for j in range(AZ_MAX):
            data[i][j] = measPower(FREQ_MIN, FREQ_MAX, INTEGRATION_INTERVAL, GAIN)
            moveStepper(0, -1)
            time.sleep(0.2)
    moveStepper(1, 0)

np.savetxt("ImageData" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + ".csv", data, delimiter=",")
plt.imshow(data, origin='lower', interpolation=None)
plt.show()
