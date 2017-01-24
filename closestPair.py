#!/usr/bin/python3
from itertools import combinations
from statistics import median
from sys import argv

class Pair():
    def __init__(self, x, y):
        self.x = self.int(x)
        self.y = self.int(y)

    def __eq__(self, pair):
        if isinstance(pair, self.__class__):
            return (self.x, self.y) == (pair.x, pair.y)
        return NotImplemented

    # Distance (this isn't really a subtraction... but it works for us)
    def __sub__(self, pair):
        return round(((pair.x - self.x)**2 + (pair.y - self.y)**2)**0.5, 7)

    def __add__(self, pair):  # Needed for median
        return Pair(self.x + pair.x, self.y + pair.y)

    def __truediv__(self, i):  # Needed for median
        assert(isinstance(i, int))
        return Pair(self.x / i, self.y / i)

    def __hash__(self):  # Needed for set
        return hash((self.x, self.y))

    def __lt__(self, pair):  # Needed for sorting
        if(self.x == pair.x):
            return self.y < pair.y
        return self.x < pair.x

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    @staticmethod
    def int(number):
        return round(float(number), 7)

    @staticmethod
    def order(p1, p2):
        return (min(p1, p2), max(p1, p2))

def Main():
    if(len(argv) != 2 or argv[1] not in ("brute", "basic", "optimal")):
        print("closestPair [brute|basic|optimal]")
        exit(1)

    collection = process_input()
    if(len(collection) < 2):
        print("Need to enter more than 1 point")
        exit(1)

    if(argv[1] == "brute"):
        pairs, num = brute(collection)
    elif(argv[1] == "basic"):
        pairs, num = basic(collection)
    else:
        pairs, num = optimal(collection)

    print("closest pair distance: {}".format(num))
    for pair in pairs:
        print(pair[0], " ", pair[1])

def brute(collection):
    closest_distance = float('inf')
    closest_pair = []

    for first_element, second_element in combinations(collection, 2):
            f, s = Pair.order(first_element, second_element)

            if(f - s == closest_distance):
                closest_pair.append((f, s))
            elif(f - s < closest_distance):
                closest_pair = [(f, s)]
                closest_distance = f - s

    return closest_pair, closest_pair[0][0] - closest_pair[0][1]

def basic(collection):
    return optimal(collection, False)

def optimal(collection, optimal=True):
    collection = list(set(collection))  # O(n)
    sorted_x = sorted(collection, key=lambda pair: pair.x)  # O(n log n)

    def solve(collection, sorted_y=None):
        if(len(collection) == 1):
            return [(collection[0], )]
        if(len(collection) == 2):
            return [Pair.order(collection[0], collection[1])]

        median_x = median(collection).x  # O(1)

        if(optimal):  # T(n) = 2 * T(n/2) + 2 * O(n/2)
            left = solve(collection[:len(collection) // 2], [pair for pair in sorted_y if pair.x < median_x])
            right = solve(collection[len(collection) // 2:], [pair for pair in sorted_y if pair.x > median_x])
        else:  # O(log n)
            left = solve(collection[:len(collection) // 2])
            right = solve(collection[len(collection) // 2:])

        d_1 = left[0][1] - left[0][0] if (len(left[0]) == 2) else float('inf')
        d_2 = right[0][1] - right[0][0] if (len(right[0]) == 2) else float('inf')
        d = min(d_1, d_2)

        ans = [s for side, dist in zip((left, right), (d_1, d_2)) if dist == d for s in side]

        if(optimal):  # No need to sort, already sorted in sorted_y. O(n)
            collection = [pair for pair in sorted_y if median_x - d <= pair.x <= median_x + d]
        else:  # O( n + n log n ) = O ( n log n)
            collection = [pair for pair in collection if median_x - d <= pair.x <= median_x + d]
            collection.sort(key=lambda p: p.y)

        for index, pair in enumerate(collection):  # O(n)
            j = index - 1
            x = 0
            while(j >= 0 and pair.y - collection[j].y <= d):  # O(1)
                x += 1
                if(x > 6):
                    assert(False)
                if (collection[j], pair) in ans or (pair, collection[j]) in ans:
                    pass
                elif (collection[j] - pair == d):
                    ans.append(Pair.order(collection[j], pair))
                elif(collection[j] - pair < d):
                    ans = [Pair.order(collection[j], pair)]
                    d = collection[j] - pair
                j -= 1
        return ans

    if(optimal):
        sorted_y = sorted(collection, key=lambda pair: pair.y)  # O(n log n)
        ans = sorted(solve(sorted_x, sorted_y))
        return ans, ans[0][0] - ans[0][1]
    else:
        ans = sorted(solve(sorted_x))
        return ans, ans[0][0] - ans[0][1]

def process_input():
    collection = []
    try:  # Breaks on <CTRL-D>
        while(True):
            couple = input().split()
            try:  # Breaks on shitty input
                s = [float(x) for x in couple]
                collection.append(Pair(*s))
            except:
                pass
    except:
        return sorted(collection)


if __name__ == "__main__":
    Main()
