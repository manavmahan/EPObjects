import pandas as pd

from EnumTypes import SurfaceType
from GeometryObject.XYZList import XYZList

from IDFObject.Construction import Construction
from IDFObject.IDFObject import IDFObject

class Detailed(IDFObject):
    __IDFName__ = "FenestrationSurface:Detailed"
    Properties = [
        'Name',
        'SurfaceType',
        'ConstructionName',
        'BuildingSurfaceName',
        'OutsideBoundaryConditionObject',
        'ViewFactor',
        'FrameAndDividerName',
        'Multiplier',
        'XYZs',
    ]
    
    __area = None
    @property
    def Area(self):
        if not self.__area:
            self.__area = self.XYZs.Area
        return self.__area

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)
        self.Initialise()

    def Initialise(self):
        if not hasattr(self, 'XYZs'):
            return

        if self.Properties.XYZs == None:
            raise Exception(f"Cannot iniialise XYZs for {self.Properties.Name}!")

        if isinstance(self.Properties.XYZs, str):
            self.Properties.XYZs = XYZList(self.Properties.XYZs)

Detailed.ExternalWindow = dict(
    SurfaceType = SurfaceType.Window,
    ConstructionName = Construction.Glazing['Name'],
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
    FrameAndDividerName = '',
    Multiplier = '',
)