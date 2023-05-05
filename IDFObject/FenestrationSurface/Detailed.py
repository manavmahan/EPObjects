import pandas as pd
import numpy as np

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
    
    @property
    def Area(self):
        return self.XYZs.Area

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)
        self.Initialise()

    def Initialise(self):
        if not hasattr(self, 'XYZs'):
            raise Exception(f"Cannot iniialise XYZs for {self.Name}!")

        if isinstance(self.XYZs, (str, np.ndarray)):
            self.XYZs = XYZList(self.XYZs)
            return

        if self.XYZs == None:
            raise Exception(f"Cannot iniialise XYZs for {self.Name}!")


Detailed.ExternalWindow = dict(
    SurfaceType = SurfaceType.Window,
    ConstructionName = Construction.Glazing['Name'],
    OutsideBoundaryConditionObject = '',
    ViewFactor = '',
    FrameAndDividerName = '',
    Multiplier = '',
)