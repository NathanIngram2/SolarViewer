import subprocess as sp
import pandas as pd

from solar_viewer_utilities import info, warn, error

while 1:
    info("Starting rtl_power")
    rst = sp.run(["rtl_power -f 980M:1020M:128k -g 0 -i 1s -1 tmp/rtl_power_out.csv"], capture_output=True, text=True)
    info("Done rtl_power")
    raw = pd.read_csv("tmp/rtl_power_out.csv")
    proc = raw.iloc[:, 0:4]
    proc[len(proc.columns)] = raw.iloc[:, 6:-1].mean(axis=1)
    mean_all_freq_and_time = proc.iloc[:, 4].mean()

    warn("Power: " + str(mean_all_freq_and_time))

info("Exiting...")
