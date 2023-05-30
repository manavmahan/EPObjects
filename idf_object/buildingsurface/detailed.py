import math
import numpy as np

from enum_types import Direction, SurfaceType

from geometry_object.xyzlist import XYZList

from idf_object.construction import Construction
from idf_object.fenestrationsurface.detailed import Detailed as Fenestration
from idf_object import IDFObject
from idf_object.zonelist import ZoneList

class Detailed(IDFObject):
    __IDFName__ = "BuildingSurface:Detailed"
    Properties = [
        'Name',
        'SurfaceType',
        'ConstructionName',
        'ZoneName',
        'SpaceName',
        'OutsideBoundaryCondition',
        'OutsideBoundaryConditionObject',
        'SunExposure',
        'WindExposure',
        'ViewFactor',
        'XYZs',
    ]
    
    @property
    def Area(self):
        if not self.__area:
            self.__area = self.XYZs.Area
        return self.__area
    
    @property
    def NetArea(self):
        if not self.__netArea:
            self.__netArea = self.Area
            if (self.FenestrationArea):
                self.__netArea -= self.FenestrationArea
        return self.__netArea

    @property
    def Direction(self):
        return self.__direction

    @property
    def FenestrationArea(self):
        return self.__fenestrationArea

    @FenestrationArea.setter
    def FenestrationArea(self, value):
        self.__fenestrationArea = value
        self.__area = None

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)

        self.__area = None
        self.__netArea = None
        self.__direction = None
        self.__fenestrationArea = None
        self.Initialise()

    def Initialise(self):
        if not hasattr(self, 'XYZs'):
            raise Exception(f"Cannot initialise XYZs for {self.Properties['Name']}!")

        if self.XYZs is None:
            raise Exception(f"Cannot initialise XYZs for {self.Properties['Name']}!")

        if isinstance(self.XYZs, (str, np.ndarray)):
            self.XYZs = XYZList(self.XYZs)

        if isinstance(self.SurfaceType, str):
            self.SurfaceType = SurfaceType(self.SurfaceType)
        
        if self.SurfaceType == SurfaceType.Wall:
            if -math.pi/4 < self.XYZs.plane.angle_from_xaxis <= math.pi/4:
                self.__direction = Direction.E
            
            if -3 * math.pi/4 < self.XYZs.plane.angle_from_xaxis <= -math.pi/4:
                self.__direction = Direction.S

            if self.XYZs.plane.angle_from_xaxis <= -3 * math.pi/4 or self.XYZs.plane.angle_from_xaxis > 3 * math.pi/4:
                self.__direction = Direction.W

            if math.pi/4 < self.XYZs.plane.angle_from_xaxis <= 3 * math.pi/4:
                self.__direction = Direction.N

            # if not self.Name.endswith(str(self.Direction)): self.Name += f'.{self.Direction}'

Detailed.ExternalWall = dict(
    SurfaceType = SurfaceType.Wall,
    ConstructionName = Construction.WallExternal['Name'],
    OutsideBoundaryCondition = 'Outdoors',
    SunExposure = 'SunExposed',
    WindExposure = 'WindExposed',
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
)

Detailed.FloorInternal = dict(
    SurfaceType = SurfaceType.Floor,
    ConstructionName = Construction.FloorInternal['Name'],
    OutsideBoundaryCondition = 'Adiabatic',
    SunExposure = 'NoSun',
    WindExposure = 'NoWind',
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
)

Detailed.FloorGround = dict(
    SurfaceType = SurfaceType.Floor,
    ConstructionName = Construction.FloorGround['Name'],
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