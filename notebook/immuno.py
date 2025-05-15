import utils
import numpy as np
import matplotlib.pyplot as plt
import sys
import collections
import statistics
import re


def key(D):
    params, time, volume, status, path = D
    return max(volume) if status == 0 else 0


def volume(D):
    params, time, volume, *rest = D
    return max(volume) / volume[0]


def experiment():
    E = utils.experiment("data.new.xlsx")
    for (typ, name), (time, volume) in E.items():
        if re.match("control_[0123]", name) and typ == "4T1":
            volume0 = volume[0]
            color = utils.color[typ]
            plt.plot(time, np.divide(volume, volume0), color + 'o-', alpha=0.5)


D = sorted(utils.read11("."), key=key)
if D == []:
    sys.stderr.write("immuno.py: error: no data, run `tar zxf 1.tar.gz`\n")
    sys.exit(1)
mvolume = (volume(d) for d in D)
*rest, volume_max = statistics.quantiles(mvolume, n=50)
Status = collections.Counter()
cnt = 0
for params, time, volume, status, path in D:
    time = np.divide(time, 60 * 60 * 24)
    volume = np.divide(volume, volume[0])
    Status[status] += 1
    color = "k" if status == 0 else "b"
    plt.plot(time, volume, color, alpha=0.5)
    if params["includeImmuno"]:
        location = params["location1"]
        index = np.searchsorted(time, location)
        if index < len(volume):
            plt.plot([location], [volume[index]], "k")
    cnt += 1
    if cnt % 35 == 0:
        path = f"immuno.{cnt:05}.png"
        sys.stderr.write(f"immuno.py: {path}\n")
        # plt.yscale("log")
        plt.xlabel("time (days)")
        plt.ylabel("relative tumor volume")
        # experiment()
        plt.axis([0, None, 0, volume_max])
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
sys.stderr.write(f"simulatins     status\n")
for k in sorted(Status):
    sys.stderr.write(f"{Status[k]:10} {k:10}\n")
