import numpy as np
from scipy.spatial.transform import Rotation

from .Plane import Plane
from .XYZ import XYZ

class XYZList:
    XYZs = np.empty(shape=(0,3))

    __round = 5

    __area = None
    @property
    def Area(self,):
        if self.__area is None:
            self.__area = self.GetArea()
        return 0.5 * np.abs(self.__area)

    @property
    def IsCounterClockwise(self,):
        if self.__area is None:
            self.__area = self.GetArea()
        return self.__area < 0

    __plane = None
    @property
    def Plane(self):
        if self.__plane is not None:
            return Plane

        if self.XYZs.shape[0] < 2:
            return None
        __plane = Plane(XYZ(self.XYZs[0]), XYZ(self.XYZs[1]), XYZ(self.XYZs[2]))
        return __plane

    def __call__(self, *args, **kwds):
        return self.XYZs(*args, **kwds)

    def __init__(self, *xyzs) -> None:
        if isinstance(xyzs[0], str):
            xyzsNew = np.array(xyzs[0].split(';')[1:], dtype=np.float16).reshape(-1,3)
        else:
            xyzsNew = np.copy(xyzs)
        for xyz in xyzsNew:
            self.AddXYZ(xyz)

    def __str__(self) -> str:
        return f'''{len(self.XYZs)},{','.join(str(XYZ(p)) for p in self.XYZs)}'''

    def AddXYZ(self, xyz):
        if isinstance(xyz, XYZ):
            self.XYZs = np.concatenate((self.XYZs, xyz.Coords.reshape(-1, 3)), axis=0)
        elif isinstance(xyz, np.ndarray):
            if len(xyz) == 3:
                self.XYZs = np.concatenate((self.XYZs, xyz.reshape(-1, 3)), axis=0)
            elif xyz.shape[1] == 3:
                self.XYZs = np.concatenate((self.XYZs, xyz), axis=0)
            else:
                raise Exception(f"Invalid argument type: {xyz}")
        else:
            raise Exception(f"Invalid argument type: {xyz}")

    def ChangeZCoordinate(self, z: float) -> None:
        self.XYZs[:, 2] = round(z, self.__round)

    def Copy(self):
        return XYZList(self.XYZs)

    def DisplaceToOrigin(self):
        min = self.XYZs.min(axis=0)
        self.XYZs = self.XYZs - min

    def Flip(self):
        self.XYZs = np.flip(self.XYZs, axis=0)

    def GetArea(self):
        if self.Plane is None:
            return None

        for x in self.XYZs[3:]:
            if self.Plane.IsOnPlane(x):
                raise Exception(f"All points are not co-planar. Plane: {self.Plane.Normal}, Point: {x}")

        rotation = self.Plane.RotationMatrix()
        xyzs = rotation.apply(self.XYZs) if rotation is not None else self.XYZs
        x = xyzs[:, 0]
        y = xyzs[:, 1]
        return np.round(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)), 5)

    def Rotate(self, angle: float, axis=np.array((0, 0, 1))):
        matrix = Rotation.from_rotvec(angle * axis)
        self.XYZs = matrix.apply(self.XYZs)