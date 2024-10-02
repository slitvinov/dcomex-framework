import utils
import numpy as np
import matplotlib.pyplot as plt

cnt = 0
for params, time, volume, status in utils.read11("1.tar.gz"):
    time = np.divide(time, 60 * 60 * 24)
    volume = np.divide(volume, volume[0])
    location = params["location"]
    index = np.searchsorted(time, location)
    style = "k-" if status == 0 else "r-"
    plt.plot(time, volume, style, alpha=0.5)
    if index < len(volume):
        plt.plot([location], [volume[index]], "ok", alpha=0.5)
    cnt += 1
    if cnt % 10 == 0:
        path = f"immuno.{cnt:05}.png"
        print(path)
        plt.yscale("log")
        plt.xlabel("time (days)")
        plt.ylabel("relative tumor volume (log scale)")
        plt.axis([None, None, 1, 100])
        plt.savefig(path)
        plt.close()
