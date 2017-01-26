import unittest
import sys
from closestPair import Pair, process_input, brute, basic, optimal
import random
import os
import logging

def monkeypatch(fnct):
    def first_element(*args, **kw):
        return sorted(list(set(fnct(*args, **kw)[0])))
    return first_element

brute = monkeypatch(brute)
basic = monkeypatch(basic)
optimal = monkeypatch(optimal)


class TestClosestPairFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.set_of_basic_collections = [
            [Pair(1, 1), Pair(2, 2)],
            [Pair(1, 1), Pair(2, 2), Pair(-10000, 10000)],
            [Pair(1, 1), Pair(2, 2), Pair(500, 500), Pair(-10000, 10000)],
            [Pair(1, 1), Pair(2, 2), Pair(500, 500), Pair(-10000, 10000), Pair(-10000, -10000)],
            [Pair(1, 1), Pair(2, 2), Pair(500, 500), Pair(-10000, 10000), Pair(-10000, -10000), Pair(100, 100)]

        ]
        self.w = Pair(1.12345677, -1)
        self.x = Pair(1.12345679, -1)
        self.y = Pair(1.12345671, -1)
        self.z = Pair(1, 1)

        self.fncts = (brute, basic, optimal)
        assert(sys.version_info > (3, 0))

    def test_equality(self):
        self.assertEqual(Pair(1.12345677, -1), Pair(1.12345679, -1))

    def test_inequality(self):
        self.assertFalse(Pair(1.12345679, -1) == Pair(1.12345671, -1))

    def test_all_basic_inputs(self):
        for fnct in self.fncts:
            for collection in self.set_of_basic_collections:
                log = logging.getLogger("test_basic_inputs")
                log.debug("Function= {}".format(fnct.__qualname__))
                log.debug(collection)
                self.assertEqual([(collection[0], collection[1])], fnct(collection))
                self.assertEqual([(collection[0], collection[1])], fnct(collection[::-1]))

    def test_multiple(self):
        collection = [Pair(1, 1), Pair(2, 2), Pair(3, 3)]
        self.assertEqual([(collection[0], collection[1]), (collection[1], collection[2])], brute(collection))
        self.assertEqual([(collection[0], collection[1]), (collection[1], collection[2])], basic(collection))
        self.assertEqual([(collection[0], collection[1]), (collection[1], collection[2])], optimal(collection))

    def test_a_bunch_of_random(self):
        random.seed(int.from_bytes(os.urandom(4), byteorder="big"))
        for _ in range(20):
            collection = []
            for _ in range(100):
                collection.append(Pair(random.uniform(-10000, 10000), random.uniform(-10000, 10000)))
            self.assertEqual(basic(collection), brute(collection))
            self.assertEqual(basic(collection), optimal(collection))

    def test_10_by_10(self):
        collection = []
        for x in range(10):
            for y in range(10):
                collection.append(Pair(x, y))
        self.assertEqual(basic(collection), brute(collection))
        self.assertEqual(optimal(collection), brute(collection))

    def test_vertical(self):
        collection = [Pair(0, 0), Pair(0, 1), Pair(0, 2), Pair(0, 3), Pair(0, 10)]
        self.assertEqual(basic(collection), brute(collection))
        self.assertEqual(optimal(collection), brute(collection))
        collection.pop()
        self.assertEqual(basic(collection), brute(collection))
        self.assertEqual(optimal(collection), brute(collection))

    def test_horizontal(self):
        collection = [Pair(0, 0), Pair(1, 0), Pair(2, 0), Pair(3, 0), Pair(4, 0)]
        self.assertEqual(basic(collection), brute(collection))
        self.assertEqual(optimal(collection), brute(collection))
        collection.pop()
        self.assertEqual(basic(collection), brute(collection))
        self.assertEqual(optimal(collection), brute(collection))

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("test_basic_inputs").setLevel(logging.NOTSET)

    unittest.main()
