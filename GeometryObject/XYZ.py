import numpy as np
from scipy.spatial.transform import Rotation

class XYZ:
    __round = 5
    Coords = np.zeros((3), dtype=np.float64)

    def __call__(self, *args, **kwds):
        return self.Coords(*args, **kwds)

    def __init__(self, *args) -> None:
        if len(args) == 0:
            return

        if isinstance(args[0], str):
            coords = args[0]
            if ';' in coords:
                coords = coords.split(';')
            elif ',' in coords:
                coords = coords.split(',')
            coords = np.array(coords, dtype=np.float64)
            self.Coords = coords
            return 

        if len(args) == 1:
            self.Coords = np.round(args[0], self.__round)
        elif len(args) == 3:
            self.Coords = np.round(args, self.__round)

    def __mul__(self, a):
        return self.Coords * a.Coords

    def __str__(self) -> str:
        return ','.join(str(x) for x in self.Coords)

    def __repr__(self) -> str:
        return self.__str__()

    def ChangeZCoordinate(self, z: float) -> None:
        self.Coords[2] = round(z, self.__round)

    def Distance(self, point):
        return np.sqrt(np.sum(np.square(self - point)))

    def DistanceFromLine(self, line):
        p1 = line[0]
        p2 = line[1]
        return np.linalg.norm(np.cross(p2-p1, p1-self.Coords))/np.linalg.norm(p2-p1)

    def IncreaseHeight(self, h: float) -> None:
        self.Coords[2] += round(h, self.__round)

    def Move(self, newOrigin):
        if isinstance(newOrigin, XYZ):
            value = newOrigin.Coords
        if isinstance(newOrigin, np.ndarray):
            value = newOrigin
        return XYZ(self.Coords - value)

    def Rotate(self, angle: float, axis=np.array((0, 0, 1))):
        matrix = Rotation.from_rotvec(angle * axis)
        return XYZ(matrix.apply(self.Coords))

XYZ.Origin = XYZ()
XYZ.XAxis = XYZ(1, 0, 0)
XYZ.YAxis = XYZ(0, 1, 0)
XYZ.ZAxis = XYZ(0, 0, 1)