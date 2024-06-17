import math
import graph
import matplotlib.pyplot as plt
import random
import timeit
import os
import time


def elli(x):
    time.sleep(0.01)
    n = len(x)
    return math.fsum(1e6**(i / (n - 1)) * x[i]**2 for i in range(n))


def run():
    return graph.cmaes(elli,
                       10 * [0.1],
                       1,
                       167,
                       Random=random.Random(12345),
                       workers=workers)


for workers in None, 1, 2, 4, 8:
    print(workers, timeit.timeit(run, number=1))
