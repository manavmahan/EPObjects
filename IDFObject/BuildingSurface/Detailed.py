import pandas as pd
from GeometryObject import XYZList
from IDFObject import IDFObject

class Detailed(IDFObject.IDFObject):
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
        return self.__area

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)
        self.Initialise()

    def Initialise(self):
        if self.XYZs is None:
            raise Exception(f"Cannot iniialise XYZs for {self.Properties['Name']}!")

        if isinstance(self.XYZs, str):
            self.XYZs = XYZList.XYZList(self.XYZs)