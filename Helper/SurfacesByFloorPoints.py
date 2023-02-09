import math
import numpy as np

from EnumTypes import SurfaceType

from GeometryObject.XYZ import XYZ
from GeometryObject.XYZList import XYZList

from IDFObject.BuildingSurface.Detailed import Detailed
from IDFObject.FenestrationSurface.Detailed import Detailed as Window

def CreatelWallsByPointsAndHeight(points: XYZList, height: float, zoneName: str) -> list:
    surfaces = []
    for p1, p2 in zip(np.roll(points.XYZs, 1, axis=0), points.XYZs,):
        p1 = XYZ(p1)
        p2 = XYZ(p2)
        
        p3 = XYZ(p2.Coords)
        p3.IncreaseHeight(height)
        
        p4 = XYZ(p1.Coords)
        p4.IncreaseHeight(height)

        wall = dict(Detailed.ExternalWall)
        wall.update(
            dict(
                Name = f'{zoneName}.Wall.{len(surfaces)}',
                XYZs = XYZList([p1, p2, p3, p4]),
                ZoneName = zoneName,
            )
        )

        surface = Detailed(wall)
        surfaces += [surface]
    return surfaces

def CreateWallsByPointsHeightAndFloorCount(points: XYZList, height: float, floorCount: int)-> list:
    surfaces = []
    for i in range(floorCount):
        points = XYZList(points.XYZs)
        for p in points.XYZs:
            p[2] = i * height
        surfaces += CreatelWallsByPointsAndHeight(points, height, f'Office.{i}.0')
    return surfaces

def CreateFenestration(wall: Detailed, wwr: float, count: int = 1)-> list():
    openingFactor = math.sqrt(wwr / count)
    for i in range(count):
        mid = 0.5 * (wall.XYZs.XYZs[0] + wall.XYZs.XYZs[2])
        
        window = dict(Window.ExternalWindow)
        window.update(
            dict(
                Name = f'{wall.Name}.window.{i}',
                BuildingSurfaceName = wall.Name,
                XYZs = XYZList(np.array([mid + (v - mid) * openingFactor for v in wall.XYZs.XYZs]))
            )
        )

        window = Window(window)
        wall.FenestrationArea = window.Area
        yield window

def CreateFloors(points: XYZList, height: float, floorCount: int)-> list:
    surfaces = []
    for i in range(floorCount):
        if i==0:
            surface = dict(Detailed.GroundFloor)
        else:
            surface = dict(Detailed.FloorCeiling)
            surface["OutsideBoundaryCondition"] = 'Zone'
            surface["OutsideBoundaryConditionObject"] = f'Office.{i-1}.0'

        points1 = points.Copy()
        points1.Flip()
        points1.ChangeZCoordinate(i * height)
        
        surface["ZoneName"] = f'Office.{i}.0'
        surface["Name"] = f'Office.{i}.0.Floor'
        surface["XYZs"] = points1
        surfaces += [Detailed(surface)]
    return surfaces

def CreateRoof(points: XYZList, height: float, floorCount: int)-> list:
    surfaces = []
    points = XYZList(points.XYZs)
    points.ChangeZCoordinate(floorCount * height)
    surface = dict(Detailed.Roof)
    surface["ZoneName"] = f'Office.{floorCount-1}.0'
    surface["Name"] = f'Office.{floorCount-1}.0.Roof'
    surface["XYZs"] = points
    surfaces += [Detailed(surface)]
    return surfaces