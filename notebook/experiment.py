import utils
import numpy as np
import matplotlib.pyplot as plt
import sys
import re

plt.yscale("log")
plt.xlabel("time (days)")
plt.ylabel("relative tumor volume (log scale)")
E = utils.experiment("data.xlsx")
for (typ, name), (time, volume) in E.items():
    if re.match("^control", name):
        time0 = utils.tstart[typ]
        color = utils.color[typ]
        try:
            i = time.index(time0)
            volume0 = volume[i]
        except ValueError:
            volume0, = np.interp([time0], time, volume)
        plt.plot(np.subtract(time, time0),
                 np.divide(volume, volume0),
                 color + 'o-',
                 alpha=0.5)
plt.axis([0, None, 1, 200])
plt.show()
