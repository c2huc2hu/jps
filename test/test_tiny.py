from test.utils import *
import jps.jps_refactored as jps

class JPSTinyTests(unittest.TestCase):
    "Test JPS on the tiny map"

    def setUp(self):
        self.map = pad_arr(load_map('test/maps/tiny.map'))
        self.j = jps.JPSField(self.map, 1, 1)

    def test_bad_start(self):
        with self.assertRaises(ValueError):
            self.j = jps.JPSField(self.map, 0, 0)

    def test_bad_end(self):
        with self.assertRaises(ValueError):
            self.j.get_full_path({(4, 4)})

    def test_zero(self):
        self.assertEqual([(1, 1)], self.j.get_full_path({(1, 1)}))
        self.assertEqual([(1, 1)], self.j.get_jump_point_path({(1, 1)}))
        self.assertEqual(0, self.j.get_path_length({(1, 1)}))

    def test_corner_cut(self):
        corner_cut_result = jps.JPSField(self.map, 1, 1, corner_cut=True, diagonal_cost=1.4)
        self.assertEqual(corner_cut_result.get_path_length({(3, 1)}), 2 + 2 * 1.4)
        self.assertEqual(corner_cut_result.get_jump_point_path({(3, 1)}), [(1, 1), (1, 2), (2, 3), (3, 2), (3, 1)])
        self.assertEqual(corner_cut_result.get_full_path({(3, 1)}), [(1, 1), (1, 2), (2, 3), (3, 2), (3, 1)])

    def test_no_corner_cut(self):
        no_corner_cut_result = jps.JPSField(self.map, 1, 1, corner_cut=False)
        self.assertEqual(no_corner_cut_result.get_path_length({(3, 1)}), 6)
        self.assertEqual(no_corner_cut_result.get_full_path({(3, 1)}), [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1)])
        self.assertEqual(no_corner_cut_result.get_jump_point_path({(3, 1)}), [(1, 1), (1, 3), (3, 3), (3, 1)])

    def test_resumable(self):
        resumable_j = jps.JPSField(self.map, 1, 1, resumable=True)
        resumable_j.get_jump_point_path({(1, 3)})
        resumable_j.get_jump_point_path({(3, 3)})

if __name__ == '__main__':
    unittest.main()