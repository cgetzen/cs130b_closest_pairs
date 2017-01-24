#!/usr/bin/python3
import bisect
import math
import time
from itertools import combinations
from statistics import median
from sys import argv

class Pair():
    def __init__(self, x, y):
        self.x = self.int(x)
        self.y = self.int(y)
        # Make sure it is a number:
        x+y+1

    def __eq__(self, pair):
        if isinstance(pair, self.__class__):
            return (self.x, self.y) == (pair.x, pair.y)
        return NotImplemented

    # Distance
    def __sub__(self, pair):
        return round( ( (pair.x - self.x)**2 + (pair.y - self.y)**2 )**0.5, 7)

    # Define Add
    def __add__(self, pair):
        return Pair(self.x + pair.x, self.y + pair.y)

    def __truediv__(self, i):
        assert(isinstance(i, int))
        return Pair(self.x/i, self.y/i)

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def int(number):
        x = int(number * 10**7) / 10 ** 7
        try:
            dec = str(number).split(".")[1]
            if(int(dec[7]) in range(5, 10)):
                return x + 0.0000001
            return x
        except:
            return x

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    # Used for sorting!
    def __lt__(self, pair):
        if(self.x == pair.x):
            return self.y < pair.y
        return self.x < pair.x


def Main():
    if(len(argv) != 2 or argv[1] not in ("brute", "basic", "optimal")):
        print("closestPair [brute|basic|optimal]")
        exit(1)

    collection = process_input()

    if(argv[1] == "brute"):
        pairs, num = brute(collection)
    elif(argv[1] == "basic"):
        pairs, num = basic(collection)
    elif(argv[1] == "optimal"):
        pairs, num = optimal(collection)

    print("closest pair distance: {}".format(num))
    print_pairs(pairs)

def print_pairs(pairs):
    for pair in pairs:
        print(pair[0], "\t", pair[1])

def brute(collection):
    """ O( n^2 ) """
    closest_distance = float('inf')
    closest_pair = []


    for first_element, second_element in combinations(collection, 2):

            f, s = min(first_element, second_element), max(first_element, second_element)

            if(f - s == closest_distance ):
                closest_pair.append((f, s))

            elif(f - s < closest_distance):
                closest_pair = [(f, s)]
                closest_distance = f - s

    return closest_pair, closest_pair[0][0] - closest_pair[0][1]

def basic(collection):
    return optimal(collection, False)

def optimal(collection, optimal = True):
    collection = list(set(collection)) # O(n)
    sorted_x = sorted(collection, key = lambda pair: pair.x) # O(n log n)
    if(optimal):
        sorted_y = sorted(collection, key = lambda pair: pair.y) # O(n log n)

    def solve(collection, sorted_y=None):
        if(len(collection) == 1): return [(collection[0])]
        if(len(collection) == 2): return [(min(collection[0], collection[1]), max(collection[0], collection[1]))]

        # O(1)
        median_x = median(collection).x

        if(optimal):
            # T(n) = 2 * T(n/2) + 2 * O(n/2)
            left = solve(collection[ :int(math.ceil(len(collection)/2))], [pair for pair in sorted_y if pair.x <= median_x])
            right = solve(collection[ int(math.floor(len(collection)/2)):], [pair for pair in sorted_y if pair.x >= median_x])
        else:
            # O(log n)
            left =  solve( collection[:int(math.ceil( len(collection)/2)) ])
            right = solve( collection[ int(math.floor(len(collection)/2)):])

        d_1 = left[0][1] - left[0][0] if (len(left[0]) == 2) else float('inf')
        d_2 = right[0][1] - right[0][0] if (len(right[0]) == 2) else float('inf')
        d = min(d_1, d_2)

        ans = []
        if(d == d_1): ans += left
        if(d == d_2): ans += right

        if(optimal):
            # No need to sort, already sorted in sorted_y
            # O( n )
            collection = [pair for pair in sorted_y if median_x - d <= pair.x <= median_x + d]
        else:
            # O( n + n log n ) = O ( n log n)
            collection = [pair for pair in collection if median_x - d <= pair.x <= median_x + d]
            collection.sort(key = lambda p: p.y)

        # O(n)
        for index, pair in enumerate(collection):
            j = index - 1
            x = 0
            # O(5) = O(1)
            while(j >= 0 and pair.y - collection[j].y <= d):
                x+=1
                if(x > 5): assert(False)
                if (collection[j], pair) in ans or (pair, collection[j]) in ans:
                    pass
                elif (collection[j] - pair == d):
                    ans.append( (min(collection[j], pair), max(collection[j], pair)))
                elif( collection[j] - pair < d):
                    ans = [(min(collection[j], pair), max(collection[j], pair))]
                    d = collection[j] - pair
                j -= 1
        return sorted(ans), ans[0][0] - ans[0][1]

    if(optimal):
        return solve(sorted_x, sorted_y)
    else:
        return solve(sorted_x)



def process_input():
    """ O( n log n ) """
    collection = []

    # O( n )
    try: # Breaks on <CTRL-D>
        while(True):
            couple = input().split()
            try: # Breaks on shitty input
                s = [float(x) for x in couple]
                bisect.insort_left(collection, Pair(*s))
                #collection.append(Pair(*s))
            except:
                pass
    except:
        pass

    # O( n log n )
    return sorted(collection)


if __name__ == "__main__":
    Main()
