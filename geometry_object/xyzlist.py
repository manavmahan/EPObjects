import numpy as np
from scipy.spatial.transform import Rotation
from shapely.geometry import LinearRing
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from geometry_object.plane import Plane

from scipy.spatial import ConvexHull

def get_cross_product(p1, p2, p3):
    return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))

def are_counter_clockwise(p1, p2, p3):
    return np.round(get_cross_product(p1, p2, p3), 5) > 0

class XYZList:
    Round = 5

    @property
    def Area(self,):
        if not self.__area:
            self.__area = self.GetArea()
        return np.abs(self.__area)
    
    @property
    def plane(self):
        if not self.__plane:
            if self.XYZs.shape[0] < 2:
                return self.__plane
            self.__plane = Plane(*self.three_points_on_convex_hull())
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
        else:
            raise Exception(f"Invalid argument type: {xyzs}")

        xyzsNew.round(self.Round)
        indices = np.sort(np.unique(xyzsNew, axis=0, return_index=True)[1])
        self.XYZs = xyzsNew[indices]

    def three_points_on_convex_hull(self):
        initial_plane = Plane(*self.XYZs[:3])
        rotation_matrix = initial_plane.rotation_matrix
        rotated_points = self.XYZs if rotation_matrix is None else rotation_matrix.apply(self.XYZs) 

        points = []
        for i0 in range(len(rotated_points)):
            if len(points) == 3: break
            i1 = (i0+1) % len(rotated_points)
            i2 = (i0+2) % len(rotated_points)
            if are_counter_clockwise(rotated_points[i0], rotated_points[i1], rotated_points[i2]):
                points.append(self.XYZs[i1])
        if len(points) < 3:
            rotated_points = np.flip(rotated_points, axis=0)
            flipped = np.flip(self.XYZs, axis=0)
            points = []
            for i0 in range(len(rotated_points)):
                if len(points) == 3: break
                i1 = (i0+1) % len(rotated_points)
                i2 = (i0+2) % len(rotated_points)
                if are_counter_clockwise(rotated_points[i0], rotated_points[i1], rotated_points[i2]):
                    points.append(flipped[i1])
        return np.array(points)

    def is_counter_clockwise(self, reference_point):
        rotation = self.plane.rotation_matrix
        if rotation is not None:
            xyzs = rotation.apply(reference_point)
        else:
            xyzs = reference_point

        if xyzs[2] == 0: 
            raise ValueError(f'Invalid reference point {reference_point} for plane {self}. Point is on plane.')
        elif rotation is not None:
            return xyzs[2] > 0
        else:
            return xyzs[2] < self.XYZs[0, 2] if self.plane.normal[2] < 0 else xyzs[2] > self.XYZs[0, 2]
    
    def get_point_on_postive_zside(self, distance=0.1):
        rotation = self.plane.rotation_matrix
        if rotation is not None:
            q = rotation.inv()
            point =  q.apply(np.array([0, 0, distance]))
        else:
            point = np.array([0, 0, distance])
        return self.XYZs.mean(axis=0) + point

    def __str__(self) -> str:
        return f'{len(self.XYZs)},{",".join(str(x) for x in self.XYZs.reshape(-1))}'

    def ChangeZCoordinate(self, z: float) -> None:
        self.XYZs[:, 2] = round(z, self.Round)

    def Copy(self):
        return XYZList(self.XYZs)

    def DisplaceToOrigin(self):
        min = self.XYZs.min(axis=0)
        self.XYZs = self.XYZs - min

    def Flip(self):
        return XYZList(np.flip(self.XYZs, axis=0))

    def GetArea(self):
        if self.plane is None:
            return None

        for x in self.XYZs[3:]:
            if self.plane.in_on_plane(x):
                raise Exception(f"All points are not co-planar. Plane: {self.plane.normal}, Point: {x}")

        rotation = self.plane.rotation_matrix
        xyzs = rotation.apply(self.XYZs) if rotation is not None else self.XYZs
        x = xyzs[:, 0]
        y = xyzs[:, 1]
        return np.round(0.5 * (np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))), 5)

    def is_inside(self, point):
        polygon = Polygon(self.XYZs)
        return polygon.contains(Point(point))

    def Offset(self, distance: float):
        if distance > 0:
            raise NotImplementedError("This function is only available for inner offsets.")
        rotation = self.plane.rotation_matrix
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