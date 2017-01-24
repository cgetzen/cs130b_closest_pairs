#!/usr/bin/python3
# n = 10^(2, 3, 4, 5)
import random
import os
import sys
from closestPair import Pair, brute, basic, optimal
from time import clock
import matplotlib.pyplot as plt
import pickle
from math import sqrt, log2
import numpy as np
from scipy import stats

random.seed(int.from_bytes(os.urandom(4), byteorder="big"))

def graph_brute():
    """ Brute cannot get too high or it will stop responding.
        Much like my housemate """
    sizes = range(100, 1100, 100)
    data = [Pair(random.uniform(-10000, 10000), random.uniform(-10000, 10000)) for _ in range(max(sizes))]
    #
    time = []
    if(os.path.exists("brute.pickle")):
        time = pickle.load(open("brute.pickle", "rb"))
    else:
        for d in [data[:s] for s in sizes]:
            start = clock()
            brute(d)
            stop = clock()
            time.append(stop - start)
        pickle.dump(time, open("brute.pickle", "wb"))
    #
    fig = plt.figure(1)
    fig.suptitle("brute")
    plt.plot(sizes, time, 'ro')
    plt.show()
    #
    line = [sqrt(t) for t in time]
    slope, intercept, r_value, p_value, std_err = stats.linregress(sizes, line)
    plt.plot(sizes, line, 'ro')
    f = lambda x: slope * x + intercept
    plt.plot([min(sizes), max(sizes)], [f(min(sizes)), f(max(sizes))], 'k')
    plt.xlabel("X^2  R-val: {}".format(r_value))
    plt.show()


def compute_optimal_times(sizes):
    if(os.path.exists("time.pickle")):
        return pickle.load(open("time.pickle", "rb"))
    else:
        time = []
        data = [Pair(random.uniform(-10000, 10000), random.uniform(-10000, 10000)) for _ in range(max(sizes))]
        for d in [data[:s] for s in sizes]:
            t = []
            for fnct in (basic, optimal):
                start = clock()
                fnct(d)
                stop = clock()
                t.append(stop - start)
            time.append(t)
        pickle.dump(time, open("time.pickle", "wb"))
        return time

def graph_transform(time_list, line_list):
    for index, t in enumerate(time_list):
        fig = plt.figure(7 + index)
        fig.suptitle("basic" if index == 0 else "optimal")
        for i, line in enumerate(line_list):
            plt.subplot(311 + i)
            plt.plot(line, t, 'ro')
            slope, intercept, r_value, p_value, std_err = stats.linregress(line, t)
            f = lambda x: slope * x + intercept
            plt.xlabel("{} R-val: {}".format("X^2" if i == 0 else "X log X" if i == 1 else "X log^2 X", r_value))
            plt.plot([min(line), max(line)], [f(min(line)), f(max(line))], 'k')
        plt.subplots_adjust(wspace=0.25, hspace=0.43, left=0.05, bottom=0.08, right=0.90, top=0.88)
        plt.show()

def graph(time_list, sizes):
    for index, t in enumerate(time_list):
        fig = plt.figure(5 + index)
        fig.suptitle("basic" if index == 0 else "optimal")
        plt.plot(sizes, t, "ro")
        plt.subplots_adjust(wspace=0.25, hspace=0.43, left=0.05, bottom=0.08, right=0.90, top=0.88)
        plt.show()


if __name__ == "__main__":
    # Start with brute:
    graph_brute()

    # Compute times for optimal
    sizes = range(10000, 210000, 10000)
    times = compute_optimal_times(sizes)

    # Graph them with no transformations
    basic_time = [t[0] for t in times]
    optimal_time = [t[1] for t in times]
    time_list = [basic_time, optimal_time]

    graph(time_list, [s for s in sizes])

    # Transform
    line_1 = np.array([s ** 2 for s in sizes])
    line_2 = np.array([s * log2(s) for s in sizes])
    line_3 = np.array([s * log2(s)**2 for s in sizes])
    line_list = [line_1, line_2, line_3]

    graph_transform(time_list, line_list)
