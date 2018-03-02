from test.test_utils import *
import jps.jps_refactored as jps

class JPSTinyTests(unittest.TestCase):
    "Test JPS on the tiny map"

    def setUp(self):
        self.map = pad_arr(load_map('test/maps/tiny.map'))

        self.j = jps.JPSField(self.map, 1, 1)

    def test_bad_start(self):
        with self.assertRaises(ValueError):
            self.j = jps.JPSField(self.map, 1, 1)

    def test_bad_end(self):
        with self.assertRaises(ValueError):
            self.j.get_full_path(1, 1)

    def test_zero(self):
        self.assertEqual(0, self.j.get_full_path(0, 0))

    def test_corner_cut(self):
        corner_cut_result = jps.jps(self.map, 0, 0, corner_cut=True, diagonal_cost=1.4)
        self.assertEqual(len(self.j.get_full_path(2, 0)), 2 + 2 * 1.4)

    def test_no_corner_cut(self):
        corner_cut_result = jps.jps(self.map, 0, 0, corner_cut=False)
        self.assertEqual(len(self.j.get_full_path(2, 0)), 6)