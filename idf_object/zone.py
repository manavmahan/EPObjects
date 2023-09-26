import numpy as np

from enum_types import Direction, SurfaceType

from geometry_object.xyzlist import XYZList

from idf_object.buildingsurface.detailed import Detailed as Surface
from idf_object.fenestrationsurface.detailed import Detailed as FenestrationSurface

from idf_object.daylighting.controls import Controls
from idf_object.daylighting.referencepoint import ReferencePoint

from idf_object.hvactemplate.zone.watertoairheatpump import WaterToAirHeatPump

from idf_object import IDFObject

from idf_object.internalmass import InternalMass

from idf_object.people import People

from idf_object.windowshadingcontrol import WindowShadingControl

from idf_object.zoneinfiltration.designflowrate import DesignFlowRate as Infiltration

def distance_from_line(point, line):
    p1 = line[0]
    p2 = line[1]
    return np.linalg.norm(np.cross(p2-p1, p1-point))/np.linalg.norm(p2-p1)

class Zone(IDFObject):
    __IDFName__ = "Zone"
    Properties = [
        "Name"
    ]

    @property
    def ExternalSurfaceArea(self):
        return sum ([x.Area for x in self.__surfaces if x.OutsideBoundaryCondition == 'Outdoors'])

    @property
    def NetVolume(self):
        wall = next(x for x in self.__surfaces if x.SurfaceType == SurfaceType.Wall).XYZs.XYZs
        return self.FloorArea * abs(wall[0, 2] - wall[2, 2])

    @property
    def FloorArea(self):
        return sum(x.Area for x in self.__surfaces if x.ZoneName==self.Name and x.SurfaceType==SurfaceType.Floor)

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)

    @property
    def Surfaces(self):
        return self.__surfaces

    def AddSurfaces(self, surfaces: list(), fenestrations: list()):
        self.__surfaces = list()
        for surface in [x for x in surfaces if x.ZoneName == self.Name]:
            surface.Fenestrations = [x for x in fenestrations if x.BuildingSurfaceName == surface.Name]
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
        )
        control.update(Controls.Default)
        control = Controls(control)
        control.AddDLPoints([x.Name for x in epObjects], illuminance = 500,)
        epObjects += [control]
        return epObjects

    def GenerateDaylightPoints(self, distance = 3.0):
        points = []
        floors = [x for x in self.__surfaces if x.SurfaceType == SurfaceType.Floor]
        for wall in [x for x in self.__surfaces if x.SurfaceType == SurfaceType.Wall]:
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
                points += [p1]
            
            if any([f.XYZs.IsInside(p2) for f in floors]):
                points += [p2]
        
        if len(points) == 0:
            distance = distance - 0.2
            self.GenerateDaylightPoints(distance)

        points = XYZList(np.array(points))
        points.ChangeZCoordinate(0.9 + p1[2])
        return points

    def GenerateDaylightPointsBasedOnFloor(self):
        points = []
        floors = [x for x in self.__surfaces if x.SurfaceType == SurfaceType.Floor]
        walls = [x for x in self.__surfaces if x.SurfaceType == SurfaceType.Wall and x.OutsideBoundaryCondition != "Outdoors"]
        for floor in floors:
            xyz = floor.XYZs.XYZs
            for p1, p2, p3 in zip(xyz, np.roll(xyz, 1, axis=0), np.roll(xyz, 2, axis=0)):
                p = np.average(np.array([p1, p2, p3]), axis=0)
                if floor.XYZs.IsInside(p):
                    points += [p]

            p = np.average(xyz, axis=0)
            if floor.XYZs.IsInside(p):
                points += [p]
        
        for p in points:
            if any([distance_from_line(p, wall) < 0.2 for wall in walls]):
                del p

        points = XYZList(np.array(points))
        points.ChangeZCoordinate(0.9 + p[2])
        return points

    def GenerateInternalMass(self, internalMassPerFloorArea, massOfInternalMaterial):
        return InternalMass(
                Name = f"InternalMass.{self.Name}",
                ZoneName = self.Name,
                SurfaceArea = self.FloorArea * internalMassPerFloorArea / massOfInternalMaterial,
            )

    def GenerateWindowShadingControl(self):
        walls = [x for x in self.__surfaces if x.SurfaceType == SurfaceType.Wall]
        epObjects = []
        for wall in walls:
            if not hasattr(wall, "Fenestrations"):
                continue

            for fenestration in wall.Fenestrations:
                if wall.Direction == Direction.N:
                    continue
                
                wsc = dict(WindowShadingControl.Default)
                wsc1 = dict(
                    Name = f"WindowShadingControl.{fenestration.Name}",
                    ZoneName = self.Name,
                    DaylightingControlObjectName = f"DaylightControl.{self.Name}",
                    FenestrationSurfaceName = fenestration.Name,
                )
                wsc.update(wsc1)
                epObjects += [WindowShadingControl(wsc)]
        return epObjects

    def get_infiltration_object(self, ach):
        return Infiltration(
            Name = f"Infiltration for {self.Name}",
            ZoneListName = self.Name,
            ScheduleName = f"Generic.Always1",
            AirChangesperHour = ach,
        )