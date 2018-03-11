from test.utils import *
from jps.jps_refactored import JPSField
import unittest

class UtilTests(unittest.TestCase):
    "Test the utils class"

    def test_load_map(self):
        "Make sure the loader works"
        tiny_map = [
            [WALKABLE, WALKABLE, WALKABLE],
            [OBSTACLE, OBSTACLE, WALKABLE],
            [WALKABLE, WALKABLE, WALKABLE]]
        self.assertEqual(load_map('test/maps/tiny.map'), tiny_map)

    def test_pad_arr(self):
        "Make sure padding works"
        arr = [['ABC', 'DEF']]
        self.assertEqual(pad_arr(arr), [
                         [OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE],
                         [OBSTACLE, 'ABC', 'DEF', OBSTACLE],
                         [OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE],
                         ])