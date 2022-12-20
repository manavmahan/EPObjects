import math
import numpy as np
from scipy.spatial.transform import Rotation

from GeometryObject.XYZ import XYZ

class Plane:
    __round = 5
    
    @property
    def AngleFromXAxis(self):
        if self.__angleFromXAxis == None:
            self.__angleFromXAxis = math.atan2(self.Normal[1], self.Normal[0])
        return self.__angleFromXAxis

    def __init__(self, p1: XYZ, p2: XYZ, p3: XYZ):
        self.__angleFromXAxis = None
        self.Point = p1
        v1 = p2.Coords - p1.Coords
        v2 = p3.Coords - p1.Coords

        self.U = XYZ(v1 / np.linalg.norm(v1))
        self.V = XYZ(v2 / np.linalg.norm(v2))
        normal = np.cross(self.U.Coords, self.V.Coords.T)
        self.Normal = np.round(normal / np.linalg.norm(normal), self.__round)

    def IsOnPlane(self, xyz) -> bool:
        if isinstance(xyz, XYZ):
            return np.round(np.sum(np.cross(xyz.Coords - self.Point.Coords, self.Normal)), 5) == 0
        if isinstance(xyz, np.ndarray):
            return np.round(np.sum(np.cross(xyz - self.Point.Coords, self.Normal)), 5) == 0

    def RotationMatrix(self):
        if all(self.Normal[:2] == XYZ.ZAxis.Coords[:2]):
            return None
        v = np.cross(XYZ.ZAxis.Coords, self.Normal,)
        c = np.dot(XYZ.ZAxis.Coords, self.Normal,)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
        return Rotation.from_matrix(rotation_matrix)