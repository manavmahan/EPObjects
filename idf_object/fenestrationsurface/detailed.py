import pandas as pd
import numpy as np

from enum_types import SurfaceType
from geometry_object.xyzlist import XYZList

from idf_object.construction import Construction
from idf_object import IDFObject

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

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.Initialise()

    def Initialise(self):
        if not hasattr(self, 'XYZs'):
            raise Exception(f"Cannot iniialise XYZs for {self.Name}!")

        if isinstance(self.XYZs, (str, np.ndarray)):
            self.XYZs = XYZList(self.XYZs)

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