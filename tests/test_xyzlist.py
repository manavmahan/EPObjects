import numpy as np
import unittest

from geometry_object.xyzlist import XYZList

class TestCounterClockwise(unittest.TestCase):
    def setUp(self):
        self.xyplane = XYZList(
            np.array([
                [0, 0, 0,],
                [0, 5, 0,],
                [5, 5, 0,],
                [5, 0, 0,],
            ])
        )
        self.diagonal_plane = XYZList(
            np.array([
                [0, 0, 0,],
                [5, 5, 0,],
                [5, 5, 5,],
                [0, 0, 5,],
            ])
        )

    def test_XY_plane(self):
        self.assertFalse(self.xyplane.is_counter_clockwise(np.array((0, 0, 1))))
        self.assertTrue(self.xyplane.is_counter_clockwise(np.array((0, 0, -1))))
        flipped = self.xyplane.Flip()
        self.assertFalse(flipped.is_counter_clockwise(np.array((0, 0, -1))))
        self.assertTrue(flipped.is_counter_clockwise(np.array((0, 0, 1))))


    def test_diagonal_plane(self):
        self.assertTrue(self.diagonal_plane.is_counter_clockwise(np.array((5, 0, -1))))
        self.assertFalse(self.diagonal_plane.is_counter_clockwise(np.array((0, 5, 1))))
        flipped = self.diagonal_plane.Flip()
        self.assertFalse(flipped.is_counter_clockwise(np.array((5, 0, -1))))
        self.assertTrue(flipped.is_counter_clockwise(np.array((0, 5, 1))))

    def test_point_on_postive_zside(self):
        xyz = self.diagonal_plane.get_point_on_postive_zside()
        self.assertTrue(self.diagonal_plane.is_counter_clockwise(xyz))

    def test_point_on_postive_zside_xyplane(self):
        xyz = self.xyplane.get_point_on_postive_zside()
        self.assertTrue(self.xyplane.is_counter_clockwise(xyz))
        flipped = self.xyplane.Flip()
        xyz = flipped.get_point_on_postive_zside()
        self.assertTrue(flipped.is_counter_clockwise(xyz))

    def test_custom_plane(self):
        plane = XYZList('5,-8.12425,-6.56335,14.76,-8.3926,-5.53789,14.76,-13.66706,-7.39001,14.76,-12.1658,-11.48757,14.76,-7.01194,-9.5993,14.76')
        xyz = plane.get_point_on_postive_zside()
        self.assertTrue(xyz[2] > 14.76)

    def test_custom_wall(self):
        wall = XYZList('4,-12.1658,-11.48757,12.0,-13.66706,-7.39001,12.0,-13.66706,-7.39001,14.76,-12.1658,-11.48757,14.76')
        floor = XYZList('5,-7.01194,-9.5993,12.0,-12.1658,-11.48757,12.0,-13.66706,-7.39001,12.0,-8.3926,-5.53789,12.0,-8.12425,-6.56335,12.0')
        xyz = wall.get_point_on_postive_zside()
        print (xyz)
        self.assertTrue(floor.is_inside(xyz))
        
if __name__ == '__main__':
    unittest.main()