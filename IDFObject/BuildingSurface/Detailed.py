import pandas as pd

from EnumTypes import SurfaceType

from GeometryObject.XYZList import XYZList

from IDFObject.Construction import Construction
from IDFObject.IDFObject import IDFObject

class Detailed(IDFObject):
    __IDFName__ = "BuildingSurface:Detailed"
    Properties = [
        'Name',
        'SurfaceType',
        'ConstructionName',
        'ZoneName',
        'OutsideBoundaryCondition',
        'OutsideBoundaryConditionObject',
        'SunExposure',
        'WindExposure',
        'ViewFactor',
        'XYZs',
    ]
    
    __area = None
    
    @property
    def Area(self):
        if not self.__area:
            self.__area = self.Properties.XYZz.Area
            if (self.__fenestrationArea):
                self.__area -= self.__fenestrationArea
        return self.__area

    __fenestrationArea = None
    @property
    def FenestrationArea(self):
        return self.__fenestrationArea

    @FenestrationArea.setter
    def FenestrationArea(self, value):
        self.__fenestrationArea = value
        self.__area = None

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)
        self.Initialise()

    def Initialise(self):
        if not hasattr(self, 'XYZs'):
            return

        if self.XYZs is None:
            raise Exception(f"Cannot iniialise XYZs for {self.Properties['Name']}!")

        if isinstance(self.XYZs, str):
            self.XYZs = XYZList(self.XYZs)

Detailed.ExternalWall = dict(
    SurfaceType = SurfaceType.Wall,
    ConstructionName = Construction.ExternalWall['Name'],
    OutsideBoundaryCondition = 'Outdoors',
    SunExposure = 'SunExposed',
    WindExposure = 'WindExposed',
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
)

Detailed.FloorCeiling = dict(
    SurfaceType = SurfaceType.Floor,
    ConstructionName = Construction.FloorCeiling['Name'],
    OutsideBoundaryCondition = 'Adiabatic',
    SunExposure = 'NoSun',
    WindExposure = 'NoWind',
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
)

Detailed.GroundFloor = dict(
    SurfaceType = SurfaceType.Floor,
    ConstructionName = Construction.GroundFloor['Name'],
    OutsideBoundaryCondition = 'Ground',
    SunExposure = 'NoSun',
    WindExposure = 'NoWind',
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
)

Detailed.Roof = dict(
    SurfaceType = SurfaceType.Roof,
    ConstructionName = Construction.Roof['Name'],
    OutsideBoundaryCondition = 'Outdoors',
    SunExposure = 'SunExposed',
    WindExposure = 'WindExposed',
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
)