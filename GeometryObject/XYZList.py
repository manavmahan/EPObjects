import numpy as np
from scipy.spatial.transform import Rotation
from shapely.geometry import LinearRing
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from GeometryObject.Plane import Plane
from GeometryObject.XYZ import XYZ

class XYZList:
    Round = 5

    @property
    def Area(self,):
        if not self.__area:
            self.__area = self.GetArea()
        return np.abs(self.__area)

    @property
    def IsCounterClockwise(self,):
        if not self.__area:
            self.__area = self.GetArea()
        return self.__area < 0

    @property
    def Plane(self):
        if not self.__plane:
            if self.XYZs.shape[0] < 2:
                return self.__plane
            self.__plane = Plane(XYZ(self.XYZs[0]), XYZ(self.XYZs[1]), XYZ(self.XYZs[2]))
        return self.__plane

    def __call__(self, *args, **kwds):
        return self.XYZs(*args, **kwds)

    def __init__(self, xyzs) -> None:
        self.__area = None
        self.__plane = None
        if isinstance(xyzs, str):
            string = xyzs.split(',')
            xyzsNew = np.array(string[1:], dtype=np.float_).reshape(int(string[0]), 3)
        elif isinstance(xyzs, np.ndarray):
            if xyzs.shape[1] != 3: raise Exception(f"Invalid argument type: {xyzs}")
            xyzsNew = np.copy(xyzs)
        elif all (isinstance(x, XYZ) for x in xyzs):
            xyzsNew = np.empty(shape=(0, 3))
            for xyz in xyzs:
                xyzsNew = np.vstack([xyzsNew, xyz.Coords.reshape(-1, 3)],)
        else:
            raise Exception(f"Invalid argument type: {xyzs}")

        xyzsNew.round(self.Round)
        indices = np.sort(np.unique(xyzsNew, axis=0, return_index=True)[1])
        self.XYZs = xyzsNew[indices]

    def __str__(self) -> str:
        return f'''{len(self.XYZs)},{','.join(str(XYZ(p)) for p in self.XYZs)}'''

    def ChangeZCoordinate(self, z: float) -> None:
        self.XYZs[:, 2] = round(z, self.Round)

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
        return np.round(0.5 * (np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))), 5)

    def IsInside(self, point):
        polygon = Polygon(self.XYZs)
        return polygon.contains(Point(point))

    def Offset(self, distance: float):
        if distance > 0:
            raise NotImplementedError("This function is only available for inner offsets.")
        rotation = self.Plane.RotationMatrix()
        if rotation is not None:
            raise NotImplementedError("This function is only available for only planes parallel to XY.")
        xyzs = rotation.apply(self.XYZs) if rotation is not None else self.XYZs
        
        lineString = LinearRing(xyzs)
        offset = lineString.parallel_offset(distance, resolution=0, join_style=2)

        offset = np.concatenate([np.array(offset.coords), np.ones([len(offset.coords), 1]) * self.XYZs[0, 2]], axis=1)
        if rotation is not None: 
            reverseRotation = rotation.inv()
            reverseRotation.apply(offset)
        return XYZList(offset)

    def Rotate(self, angle: float, axis=np.array((0, 0, 1))):
        matrix = Rotation.from_rotvec(angle * axis)
        self.XYZs = matrix.apply(self.XYZs)