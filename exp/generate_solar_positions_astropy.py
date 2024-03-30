# -*- coding: utf-8 -*-
"""
File: socket_server.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2024-03-30
Description: Generate a pickle file containing lists of sun altitude and azimuth throughout
the period of the April 8th, 2024 eclipse.


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

import numpy as np
from astropy.time import Time
from astropy.coordinates import get_sun, AltAz, EarthLocation
import time
import datetime
import pickle


t_range = Time(['2024-04-08T15:00:00.000', '2024-04-08T22:00:00.000'])
dt = t_range[1] - t_range[0]

step = Time(['2024-04-08T15:00:00.000', '2024-04-08T15:00:10.000'])
step = step[1] - step[0]
t_lst = t_range[0] + dt * np.linspace(0., 1., int(dt/step))

#print(t)
sunPos = get_sun(t_lst)
measurementLoc = EarthLocation(lat=44.227042, lon=-76.498307)  # location of measurement (Tindal field)
relSunPos = sunPos.transform_to(
    AltAz(obstime=t_lst, location=measurementLoc))  # sun position relative to measurement location

result = np.array([t_lst.datetime, relSunPos.az.deg, relSunPos.alt.deg])

with open("./sunData/April8Eclipse.pickle", 'wb') as handle:
    pickle.dump(result, handle)


#%% Test

def getSunPickledData():
    with open("./sunData/April8Eclipse.pickle", 'rb') as handle:
        sunPos = pickle.load(handle)
    target_date = datetime.datetime.utcnow()
    idex = np.argmin(np.abs(sunPos[0] - target_date))
    return sunPos[2][idex], sunPos[1][idex]

getSunPickledData()