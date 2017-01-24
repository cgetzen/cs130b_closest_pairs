#!/usr/bin/python3
import random
import os
import sys

random.seed(int.from_bytes(os.urandom(4), byteorder="big"))

if __name__ == '__main__':
    if(len(sys.argv) != 2 or not sys.argv[1].isdecimal()):
        print("./randData [number]")
        exit(1)

    for _ in range(int(sys.argv[1])):
        print("{:.7f}\t{:.7f}".format(random.uniform(-10000, 10000), random.uniform(-10000, 10000)))
