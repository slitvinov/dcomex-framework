import utils
import numpy as np
import matplotlib.pyplot as plt

cnt = 0
for params, time, volume, status in utils.read11("a.tar.gz"):
    if status == 0:
        time = np.divide(time, 60 * 60 * 24)
        location = params["location"]
        index = np.searchsorted(time, location)
        plt.plot(time,
                 volume,
                 'k', [location], [volume[index]],
                 'ok',
                 alpha=0.5)
        cnt += 1
    if cnt == 20:
        break
plt.savefig("immuno.png")
