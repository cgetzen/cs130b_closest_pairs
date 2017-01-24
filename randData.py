#!/usr/bin/python3
import random, os, sys
random.seed(int.from_bytes(os.urandom(4), byteorder="big"))
random.uniform(-10000, 10000)

if __name__ == '__main__':
    if( len(sys.argv) == 1):
        print("{}\t{}".format(random.uniform(-10000, 10000), random.uniform(-10000, 10000)))
    else:
        for _ in range(int(sys.argv[1])):
            print("{}\t{}".format(random.uniform(-10000, 10000), random.uniform(-10000, 10000)))
