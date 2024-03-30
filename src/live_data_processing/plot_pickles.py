# -*- coding: utf-8 -*-
"""
File: plot_pickles.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2024-03-30
Description: Check if a new pickle has been writen by socket_server.py, and update graph
if new data is avaliable.


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
import matplotlib.pyplot as plt
import datetime
import glob
import os
import pickle
import time

plt.rcParams.update({'font.size': 24})
plt.rcParams['lines.markersize'] = 40

#%% Input parameters

# Heatmap
heatmap = np.zeros((8, 8))-34
az_min = 10
az_max = 20
alt_min = 10
alt_max = 20
scan_timestamp = "2024-04-08 13:55:20EDT"

# Heading
sun_az = 20
sun_alt = 20
telescope_az = 22
telescope_alt = 22

# Power plot
#base = datetime.datetime.today()
#p_date_lst = [base - datetime.timedelta(seconds=x) for x in range(60)]
#p_lst = np.sin(np.linspace(0, 16*np.pi, 60)) - 32

p_date_lst = []
p_lst = []

# Max power (list of datetime and list of maximum value from each image)
#pmax_date_lst = [base - datetime.timedelta(seconds=x) for x in range(60)]
#pmax_lst = np.sin(np.linspace(0, 16*np.pi, 60)) - 32
pmax_date_lst = np.empty(0, dtype=np.datetime64)
pmax_lst = np.empty(0, dtype=float)

#% Plotting

def plot():
    cbar_ax = fig.add_axes([0.9, 0.46, 0.02, 0.4])
    axs['A'].clear()
    axs['B'].clear()
    axs['C'].clear()
    axs['D'].clear()
    #cbar_ax.clear()
    #fig.delaxes(axs['B'])
    
    # Heatmap image
    im = axs['B'].imshow(heatmap, origin='lower', extent=(az_min, az_max, alt_min, alt_max), vmin=-34, vmax=-32)
    #fig.colorbar(im, ax=axs['B'])
    
    
    fig.colorbar(im, cax=cbar_ax)
    
    axs['B'].set_title("Scan taken at\n" + scan_timestamp)
    axs['B'].set_xlabel("Azimuth (deg)")
    axs['B'].set_ylabel("Elevation (deg)")
    
    # Heading
    axs['A'].plot(sun_az, sun_alt, 'o', color='yellow', label='Sun')
    axs['A'].plot(telescope_az, telescope_alt, 'o', color='k', markersize=20, label='Telescope Heading')
    circ = plt.Circle((telescope_az, telescope_alt), 1.5, color='k', alpha=0.25, label="Telescope Beamwidth (approx)")
    axs['A'].add_patch(circ)
    axs['A'].set_xlim(sun_az-6, sun_az+6)
    axs['A'].set_ylim(sun_alt-6, sun_alt+6)
    axs['A'].set_xlabel("Azimuth (deg)")
    axs['A'].set_ylabel("Elevation (deg)")
    axs['A'].set_title("Telescope Aim\n(Scales Approximate)")
    axs['A'].set_aspect('equal')
    #legnd = axs['A'].legend(loc="upper left")
    
    # Power
    axs['C'].plot(p_date_lst, p_lst)
    axs['C'].set_ylabel("Power (dB)")
    
    # Max power
    #axs['D'].plot(pmax_date_lst, pmax_lst)
    #axs['D'].set_ylabel("Power (dB)")
    
    plt.tight_layout(pad=1.5)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    t_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    plt.savefig(f"./images/snapshot-{t_stamp}.png", dpi=75)
    plt.pause(2)


list_of_files = glob.glob('./pickles/*.pickle') # * means all if need specific format then *.csv
while len(list_of_files) == 0: # wait until first pickle written
    time.sleep(0.5)
    list_of_files = glob.glob('./pickles/*.pickle')

fig, axs = plt.subplot_mosaic("AB;AB;AB;CC;DD")
fig.set_figwidth(18)
fig.set_figheight(14)

start = time.time()
while True:

    list_of_files = glob.glob('./pickles/*.pickle') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    last_drawn = None
    
    if last_drawn != latest_file:
        with open(latest_file, 'rb') as handle:
            b = pickle.load(handle)
        
        if b["id"] == "pt":
            telescope_az = b["telescope_az"]
            telescope_alt = b["telescope_alt"]
            sun_az = b["sun_az"]
            sun_alt = b["sun_alt"]
            p_date_lst.append(np.datetime64(b["time"].isoformat()))
            p_lst.append(b["power"])
            plot()
        if b["id"] == "im":
            heatmap = b["power"]
            plot()
        last_drawn == latest_file
    time.sleep(0.5)