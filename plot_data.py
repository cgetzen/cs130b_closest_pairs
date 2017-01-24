#!/usr/bin/python3
# n = 10^(2, 3, 4, 5)
import random, os, sys
from closestPair import Pair, brute, basic, optimal
from time import clock
import matplotlib.pyplot as plt
import pickle
random.seed(int.from_bytes(os.urandom(4), byteorder="big"))

def graph_brute():
    sizes = range(100, 1100, 100)
    data = [Pair(random.uniform(-10000, 10000), random.uniform(-10000, 10000)) for _ in range(max(sizes))]

    time = []
    for d in [data[:s] for s in sizes]:
        start = clock()
        brute(d)
        stop = clock()
        time.append(stop-start)

    plt.plot(sizes, time, 'ro')
    plt.show()





time = [] # [(basic, optimal), ...]
data = [] # [c^2, c^3, ...]
sizes = [10 ** x for x in range(1, 7)] + [300, 500, 600, 700, 800]
sizes.sort()

data = [Pair(random.uniform(-10000, 10000), random.uniform(-10000, 10000)) for _ in range(max(sizes))]

for d in [data[:s] for s in sizes]:
    t = []
    for fnct in (basic, optimal):
        start = clock()
        fnct(d)
        stop = clock()
        t.append(stop-start)
    time.append(t)


plt.plot(sizes, [t[0] for t in time], 'ro')
plt.show()

plt.plot(sizes , [t[1] for t in time], 'ro')
plt.show()

for t in time:
    print(t)


def plot_set_function():
    """ O( n ) """
    t = []
    sizes = [10 ** x for x in range(1,8)]
    lists = [ [1]*s for s in sizes]
    for l in lists:
        start = clock()
        set(l)
        stop = clock()
        t.append(stop-start)
    plt.plot(sizes, t, 'ro')
    plt.show()
