import math
import numpy as np
from scipy.spatial.transform import Rotation

zaxis = np.array([0, 0, 1])

class Plane:
    __round = 5
    
    @property
    def angle_from_xaxis(self):
        if self.__angle_from_xaxis == None:
            self.__angle_from_xaxis = math.atan2(self.normal[1], self.normal[0])
        return self.__angle_from_xaxis

    def __init__(self, *args):
        if len(args) < 3:
            print ('\n'.join(args))
            raise ValueError(f'Cannot create plane from less than three points.')
        p1, p2, p3 = args
        self.point = p1
        v1 = p2 - p1
        v2 = p3 - p1

        self.U = v1 / np.linalg.norm(v1)
        self.V = v2 / np.linalg.norm(v2)
        normal = np.cross(self.U, self.V.T)
        self.normal = np.round(normal / np.linalg.norm(normal), self.__round)
        self.__angle_from_xaxis = None

    def in_on_plane(self, xyz) -> bool:
        return np.round(np.sum(np.cross(xyz - self.point, self.normal)), 5) == 0

    @property
    def rotation_matrix(self):
        if all(self.normal == zaxis):
            return None
        if all(self.normal[:2] == zaxis[:2]) and self.normal[2] == -zaxis[2]:
            return Rotation.from_rotvec(np.pi * np.array((0, 1, 0)))
        v = np.cross(zaxis, self.normal,)
        c = np.dot(zaxis, self.normal,)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
        return Rotation.from_matrix(rotation_matrix)