import pandas as pd

from ...EnumTypes import SurfaceType
from ...GeometryObject.XYZList import XYZList

class Detailed:
    Properties = {
        'Name': None,
        'SurfaceType': None,
        'ConstructionName': None,
        'ZoneName': None,
        'OutsideBoundaryCondition': None,
        'OutsideBoundaryConditionObject': None,
        'SunExposure': None,
        'WindExposure': None,
        'ViewFactor': None,
        'XYZs': None,
    }
    
    __area = None
    @property
    def Area(self):
        if not self.__area:
            self.__area = self.Properties.XYZz.Area
        return self.__area

    def __init__(self, properties: dict()):
        for property in self.Properties.keys():
            if property in properties: self.Properties[property] = properties[property]
        self.InitialiseXYZs()
        
    def __repr__(self) -> str:
        return self.__str()

    def __str__(self) -> str:
        return f'''BuildingSurface:{self.__class__.__name__},{','.join(str(x) for x in self.Properties)};'''

    def InitialiseXYZs(self):
        if self.Properties.XYZs == None:
            raise Exception(f"Cannot iniialise XYZs for {self.Properties.Name}!")

        if isinstance(self.Properties.XYZs, str):
            self.Properties.XYZs = XYZList(self.Properties.XYZs)

def InitialiseSurface(file):
    data = pd.read_csv(file, index_col=0, float_precision='round_trip')
    for name in data.index:
        yield Detailed(name, data.loc[name].to_dict())
