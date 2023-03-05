import numpy as np

from EnumTypes import Direction, SurfaceType

from GeometryObject.XYZ import XYZ
from GeometryObject.XYZList import XYZList

from IDFObject.BuildingSurface.Detailed import Detailed as Surface
from IDFObject.FenestrationSurface.Detailed import Detailed as FenestrationSurface

from IDFObject.Daylighting.Controls import Controls
from IDFObject.Daylighting.ReferencePoint import ReferencePoint

from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump

from IDFObject.IDFObject import IDFObject

from IDFObject.InternalMass import InternalMass

from IDFObject.People import People

from IDFObject.WindowShadingControl import WindowShadingControl

class Zone(IDFObject):
    __IDFName__ = "Zone"
    Properties = [
        "Name"
    ]

    @property
    def ExternalSurfaceArea(self):
        return sum ([x.Area for x in self.__surfaces if x.OutsideBoundaryCondition == 'Outdoors' or x.OutsideBoundaryCondition == 'Ground'])

    @property
    def NetVolume(self):
        wall = next(x for x in self.__surfaces if x.ZoneName==self.Name and x.SurfaceType == SurfaceType.Wall).XYZs.XYZs
        return self.FloorArea * (wall[2][2] - wall[1][2])

    @property
    def FloorArea(self):
        return sum(x.Area for x in self.__surfaces if x.ZoneName==self.Name and x.SurfaceType==SurfaceType.Floor)

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)

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
            if any([XYZ(p).DistanceFromLine(wall) < 0.2 for wall in walls]):
                del p

        points = XYZList(np.array(points))
        points.ChangeZCoordinate(0.9 + p[2])
        return points

    def GenerateInternalMass(self, internalMassPerFloorArea, massOfInternalMaterial):
        mass = dict(
            Name = f"InternalMass.{self.Name}",
            ZoneName = self.Name,
            SurfaceArea = self.FloorArea * internalMassPerFloorArea / massOfInternalMaterial,
        )
        mass.update(InternalMass.Default)
        return [InternalMass(mass)]

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

    def GetWaterToAirHeatPumpObject(self, zonelistName):
        hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
        hvac.ZoneName = self.Name
        hvac.TemplateThermostatName = f'Thermostat.{zonelistName}'
        return hvac

    def GetPeopleObject(self, persons, zonelistName):
        people = dict(People.Zone)
        people.update(
            dict(
                Name = f"People.{self.Name}",
                ZoneListName = self.Name,
                NumberofPeopleScheduleName = f"{zonelistName}.People",
                ActivityLevelScheduleName = f"{zonelistName}.Activity",
                NumberofPeople = persons,
            )
        )
        return People(people)