import utils
import numpy as np
import matplotlib.pyplot as plt


def key(D):
    params, time, volume, status = D
    return params["k_th_tumor"]


cnt = 0
for params, time, volume, status in sorted(utils.read11("."), key=key):
    time = np.divide(time, 60 * 60 * 24)
    volume = np.divide(volume, volume[0])
    location = params["location"]
    index = np.searchsorted(time, location)
    color = "k" if status == 0 else "r"
    plt.plot(time, volume, color + "-", alpha=0.5)
    if index < len(volume):
        plt.plot([location], [volume[index]], color + "o", alpha=0.5)
    cnt += 1
    if cnt % 16 == 0:
        path = f"immuno.{cnt:05}.png"
        print(path)
        plt.yscale("log")
        plt.xlabel("time (days)")
        plt.ylabel("relative tumor volume (log scale)")
        plt.axis([None, None, 1, 100])
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
