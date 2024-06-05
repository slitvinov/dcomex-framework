import graph
import math
import random
import scipy.stats
import statistics
import sys
import matplotlib.pylab as plt
import numpy as np

def save(path):
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig(path)
    plt.close()

def fun(x):
    dev = 0.01
    coeff = -1 / (2 * dev**2)
    u = coeff * (x[0] - x[1]**2)**2
    return u


random.seed(12345)
beta = 1.0
draws = 2000
trace = graph.tmcmc(lambda x: fun(x),
                    draws, [0, 0], [1, 1],
                    beta=beta,
                    trace=True)
b =  0, 1
xx = np.linspace(*b, 100)
z = [[(-fun([x, y]))**0.3 for x in xx] for y in xx]

for i, (x, accept) in enumerate(trace):
    plt.xlim(*b)
    plt.ylim(*b)
    plt.gca().set_aspect('equal')
    plt.contour(xx, xx, z, levels=8, linewidths=3)
    plt.scatter(*zip(*x), alpha=0.5, edgecolor='none', color='k')
    save("tmcmc.%03d.png" % i)
    plt.close()
