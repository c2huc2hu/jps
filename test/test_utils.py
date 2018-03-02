import unittest
from jps.jps_refactored import JPSField

OBSTACLE = JPSField.OBSTACLE
UNINITIALIZED = JPSField.UNINITIALIZED

char_to_cell = {
    '#': OBSTACLE,
    '.': UNINITIALIZED,
}

def load_map(file):
    "Return a map from a file"
    with open(file) as f:
        return [[char_to_cell[ch] for ch in line.strip()] for line in f]

def pad_arr(arr, pad=OBSTACLE):
    "Pads a 2d array with pad. Returns a copy of arr"

    if len(arr) == 0 or len(arr[0]) == 0:
        raise ValueError('Cannot pad an empty array')

    return  [
                [pad] * (len(arr[0]) + 2),
                *[[pad, *row, pad] for row in arr],
                [pad] * (len(arr[0]) + 2),
            ]


class UtilTests(unittest.TestCase):
    "Test the utils class"

    def test_load_map(self):
        "Make sure the loader works"
        tiny_map = [
            [UNINITIALIZED, UNINITIALIZED, UNINITIALIZED],
            [OBSTACLE, OBSTACLE, UNINITIALIZED],
            [UNINITIALIZED, UNINITIALIZED, UNINITIALIZED]]
        self.assertEqual(load_map('test/maps/tiny.map'), tiny_map)

    def test_pad_arr(self):
        "Make sure padding works"
        arr = [['ABC', 'DEF']]
        self.assertEqual(pad_arr(arr), [
                         [OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE],
                         [OBSTACLE, 'ABC', 'DEF', OBSTACLE],
                         [OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE],
                         ])

if __name__ == '__main__':
    unittest.main()