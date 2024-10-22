import utils
import numpy as np
import matplotlib.pyplot as plt
import sys
import collections
import statistics
import re


def key(D):
    params, time, volume, status = D
    return max(volume) / volume[0]


def experiment():
    E = utils.experiment("data.xlsx")
    for (typ, name), (time, volume) in E.items():
        if not re.match("^control", name) and typ == "4T1":
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


D = sorted(utils.read11("."), key=key)
mvolume = (key(d) for d in D)
*rest, volume_max = statistics.quantiles(mvolume, n=200)
Status = collections.Counter()
cnt = 0
for params, time, volume, status in D:
    time = np.divide(time, 60 * 60 * 24)
    volume = np.divide(volume, volume[0])
    Status[status] += 1
    # color = "k" if status == 0 else "r"
    if status == 0:
        plt.plot(time, volume, "k", alpha=0.5)
        if params["includeImmuno"]:
            location = params["location"]
            index = np.searchsorted(time, location)
            if index < len(volume):
                plt.plot([location], [volume[index]], "k")
    cnt += 1
    if cnt % 16 == 0:
        path = f"immuno.{cnt:05}.png"
        sys.stderr.write(f"immuno.py: {path}\n")
        plt.yscale("log")
        plt.xlabel("time (days)")
        plt.ylabel("relative tumor volume (log scale)")
        experiment()
        plt.axis([0, None, 1, volume_max])
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
sys.stderr.write(f"simulatins     status\n")
for k in sorted(Status):
    sys.stderr.write(f"{Status[k]:10} {k:10}\n")
