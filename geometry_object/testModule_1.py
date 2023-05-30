import math
import numpy as np
import unittest

from geometry_object.xyzlist import XYZList

class TestXYZ(unittest.TestCase):
    origin = np.array((0,0,0))
    def testOrigin(self):
        self.assertTrue(all(np.zeros((3, )) == self.origin.Coords))
    
    def testOrigin2(self):
        self.assertEqual("0.0,0.0,0.0", str(self.origin))

    def testOrigin3(self):
        self.origin.ChangeZCoordinate(3)
        self.assertTrue(all(np.array([0, 0, 3]) == self.origin.Coords))

    def testOrigin4(self):
        self.origin.ChangeZCoordinate(0)
        self.origin.IncreaseHeight(3)
        self.assertTrue(all(np.array([0, 0, 3]) == self.origin.Coords))

    def testRotaion1(self):
        point = np.array((1, 1, 5))
        rotated = point.Rotate(math.pi/4)
        self.assertListEqual(list(rotated.Coords), list(np.array((0, 1.41421, 5).Coords)))

    def testRotaion2(self):
        point = np.array((1, 5, 1))
        rotated = point.Rotate(math.pi/4, axis=XYZ.YAxis.Coords)
        self.assertListEqual(list(rotated.Coords), list(XYZ(1.41421, 5, 0).Coords))

class TestXYZList(unittest.TestCase):
    def testInformation(self):
        xyzList = XYZList()
        xyzList.AddXYZ(XYZ(0,0,0))
        xyzList.AddXYZ(np.array([0,1,0]))
        xyzList.AddXYZ(np.array(((1,1,0), (1,0,0))))
        self.assertEqual('4,0.0,0.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,0.0,0.0', str(xyzList))

    def testArea(self):
        xyzList = XYZList(np.array(((0,0,4), (1,0,4), (1,1,4), (0,1,4))))
        self.assertAlmostEqual(xyzList.Area, 1)

    def testAreaYZPlane(self):
        xyzList = XYZList(np.array(((5,0,0), (5,0,5), (5,1,5), (5,1,0))))
        self.assertAlmostEqual(xyzList.Area, 5)

    def testAreaXYZPlane(self):
        xyzList = XYZList(np.array(((0,0,0), (1,1,0), (1,1,1), (0,0,1))))
        self.assertAlmostEqual(xyzList.Area, 1.414215)

class TestOffset(unittest.TestCase):
    # def testOffsetLeft(self):
    #     xyzList = XYZList(np.array(((0,0,4), (1,0,4), (1,1,4), (0,1,4))))
    #     self.assertRaises(NotImplementedError("This function is only available for inner offsets."), xyzList.Offset(0.25))
        
    def testOffsetRight(self):
        xyzList = XYZList(np.array(((0,0,4), (1,0,4), (1,1,4), (0,1,4))))
        offset = xyzList.Offset(-0.25)
        self.assertEqual('4,0.25,0.25,4.0,0.75,0.25,4.0,0.75,0.75,4.0,0.25,0.75,4.0', str(offset))

    # def testOffsetRightInclined(self):
    #     xyzList = XYZList(np.array(((0,0,0), (1,0,1), (1,1,1), (0,1,0))))
    #     offset = xyzList.Offset(-0.25)
    #     self.assertEqual('4,0.25,0.25,4.0,0.75,0.25,4.0,0.75,0.75,4.0,0.25,0.75,4.0', str(offset))

if __name__ == '__main__':
    unittest.main()
