from test.utils import *
import jps.jps_refactored as jps

class JPSSmallTests(unittest.TestCase):
    "Test JPS on various maps to test simple cases"

    def test_a_star(self):
        pass

    def test_fork(self):
        fork_map = pad_arr(load_map('test/maps/fork.map'))
        j = jps.JPSField(fork_map, 1, 3)
        self.assertEqual(j.get_full_path({(3, 2)}), [(1, 3), (2, 3), (2, 2), (3, 2)])

    def test_clip(self):
        "Verify that we don't clip through walls"
        clip_map = pad_arr(load_map('test/maps/clip.map'))
        corner_cut_result = jps.JPSField(clip_map, 2, 1, diagonal_cost=1.5, corner_cut=True)
        self.assertEqual(corner_cut_result.get_path_length({(1, 2)}), 3 * 1.5)

        no_corner_cut_result = jps.JPSField(clip_map, 2, 1, corner_cut=False)
        self.assertEqual(no_corner_cut_result.get_path_length({1, 2}), 6)

