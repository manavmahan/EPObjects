import pandas as pd
from GeometryObject import XYZList
from IDFObject import IDFObject

class Boiler(IDFObject.IDFObject):
    __IDFName__ = "HVACTemplate:Plant:Boiler"
    Properties = [
        'Name',
        'BoilerType',
        'Capacity',
        'Efficiency',
        'FuelType',
        'Priority',
        'SizingFactor',
        'MinimumPartLoadRatio',
        'MaximumPartLoadRatio',
        'OptimumPartLoadRatio',
        'WaterOutletUpperTemperatureLimit',
    ]
    
    Efficiency = None

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)
        self.Initialise()