import utils
import numpy as np
import matplotlib.pyplot as plt
import sys
import collections


def key(D):
    params, time, volume, status = D
    return max(volume)


Status = collections.Counter()
cnt = 0
for params, time, volume, status in sorted(utils.read11("."), key=key):
    time = np.divide(time, 60 * 60 * 24)
    volume = np.divide(volume, volume[0])
    Status[status] += 1
    color = "k" if status == 0 else "r"
    plt.plot(time, volume, color + "-", alpha=0.5)
    if params["includeImmuno"]:
        location = params["location"]
        index = np.searchsorted(time, location)
        if index < len(volume):
            plt.plot([location], [volume[index]], color + "o", alpha=0.5)
    cnt += 1
    if cnt % 16 == 0:
        path = f"immuno.{cnt:05}.png"
        sys.stderr.write(f"immuno.py: {path}\n")
        plt.yscale("log")
        plt.xlabel("time (days)")
        plt.ylabel("relative tumor volume (log scale)")
        plt.axis([None, None, 1, 100])
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
print(cnt)
for k in sorted(Status):
    print(k, Status[k])
