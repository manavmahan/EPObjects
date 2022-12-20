import numpy as np

from EnumTypes import Direction, SurfaceType

from GeometryObject.XYZ import XYZ
from GeometryObject.XYZList import XYZList

from IDFObject.BuildingSurface.Detailed import Detailed 

from IDFObject.Daylighting.Controls import Controls
from IDFObject.Daylighting.ReferencePoint import ReferencePoint

from IDFObject.IDFObject import IDFObject

from IDFObject.WindowShadingControl import WindowShadingControl

class Zone(IDFObject):
    __IDFName__ = "Zone"
    Properties = [
        "Name"
    ]

    @property
    def Surfaces(self): return self.__surfaces

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)
        self.__surfaces = list()
        self.__ceilingArea = 0
        self.__floorArea = 0
        self.__wallArea = 0
        self.__windowArea = 0
        self.__roofArea = 0

    def AddSurface(self, surface: Detailed, fenestrations: list()):
        if surface.Area == None or surface.Area == 0:
            raise Exception(f"Cannot add surface without area {surface}.")

        match surface.SurfaceType:
            case SurfaceType.Ceiling:
                self.__ceilingArea += surface.Area

            case SurfaceType.Floor:
                self.__floorArea += surface.Area
            
            case SurfaceType.Roof:
                self.__roofArea += surface.Area

            case SurfaceType.Wall:
                self.__wallArea += surface.Area
                surface.Fenestrations = [x for x in fenestrations if x.BuildingSurfaceName == surface.Name]
                self.__windowArea += sum([x.Area for x in surface.Fenestrations])

    def AddSurfaces(self, surfaces: list(), fenestrations: list()):
        for surface in [x for x in surfaces if x.ZoneName == self.Name]:
            self.AddSurface(surface, fenestrations)
            self.__surfaces += [surface]

    def GenerateDaylightControl(self, zoneListName):
        epObjects = []
        dlPoints = self.GenerateDaylightPointsBasedOnFloor().XYZs
        for i, p in enumerate(dlPoints):
            epObjects += [
                ReferencePoint(dict(
                    Name = f"DLPoint.{i}.{self.Name}",
                    ZoneName = self.Name,
                    Point = p,
                ))
            ]
        
        control = dict(
            Name = f"DaylightControl.{self.Name}",
            ZoneName = self.Name,
            AvailabilityScheduleName = f"{zoneListName}.People",
            GlareCalculationDaylightingReferencePointName = epObjects[-1].Name,
            DLPoints = [x.Name for x in epObjects],
            Illuminance = 500,
        )
        control.update(Controls.Default)
        control = Controls(control)
        epObjects += [control]
        return epObjects

    def GenerateDaylightPoints(self, distance = 3.0):
        points = XYZList()
        floors = [x for x in self.Surfaces if x.SurfaceType == SurfaceType.Floor]
        for wall in [x for x in self.Surfaces if x.SurfaceType == SurfaceType.Wall]:
            if wall.OutsideBoundaryCondition != "Outdoors":
                continue
            w1 = wall.XYZs.XYZs[0]
            w2 = wall.XYZs.XYZs[1]

            midPoint = np.average(np.array([w1, w2]), axis=0)
            direction = w2 - w1
            perpendicular = np.array([direction[1], - direction[0], 0])
            perpendicular /= np.sqrt(np.sum(np.square(perpendicular)))
            p1 = distance * perpendicular + midPoint
            p2 = - distance * perpendicular + midPoint

            if any([f.XYZs.IsInside(p1) for f in floors]):
                points.AddXYZ(p1)
            
            if any([f.XYZs.IsInside(p2) for f in floors]):
                points.AddXYZ(p2)
        
        if len(points.XYZs) == 0:
            distance = distance - 0.2
            self.GenerateDaylightPoints(distance)

        points.ChangeZCoordinate(0.9 + p1[2])
        return points

    def GenerateDaylightPointsBasedOnFloor(self):
        points = XYZList()
        floors = [x for x in self.Surfaces if x.SurfaceType == SurfaceType.Floor]
        walls = [x for x in self.Surfaces if x.SurfaceType == SurfaceType.Wall and x.OutsideBoundaryCondition != "Outdoors"]
        for floor in floors:
            xyz = floor.XYZs.XYZs
            for p1, p2, p3 in zip(xyz, np.roll(xyz, 1, axis=0), np.roll(xyz, 2, axis=0)):
                p = np.average(np.array([p1, p2, p3]), axis=0)
                if floor.XYZs.IsInside(p):
                    points.AddXYZ(p)

            p = np.average(xyz, axis=0)
            if floor.XYZs.IsInside(p):
                points.AddXYZ(p)
        
        for p in points.XYZs:
            if any([XYZ(p).DistanceFromLine(wall) < 0.2 for wall in walls]):
                del p

        points.ChangeZCoordinate(0.9 + p[2])
        return points

    def GenerateWindowShadingControl(self):
        walls = [x for x in self.Surfaces if x.SurfaceType == SurfaceType.Wall]
        epObjects = []
        for wall in walls:
            if not hasattr(wall, "Fenestrations"):
                continue

            for fenestration in wall.Fenestrations:
                if wall.Direction == Direction.N:
                    continue

                wsc = dict(
                    Name = f"WindowShadingControl.{fenestration.Name}",
                    ZoneName = self.Name,
                    DaylightingControlObjectName = f"DaylightControl.{self.Name}",
                    FenestrationSurfaceName = fenestration.Name,
                )
                wsc.update(WindowShadingControl.Default)
                wsc = WindowShadingControl(wsc)
                epObjects += [wsc]
        return epObjects