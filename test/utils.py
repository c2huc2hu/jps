import unittest
from jps.jps_refactored import JPSField

OBSTACLE = JPSField.OBSTACLE
WALKABLE = JPSField.WALKABLE

char_to_cell = {
    '#': OBSTACLE,
    '.': WALKABLE,
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