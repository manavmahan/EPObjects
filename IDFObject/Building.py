import numpy as np

from IDFObject import IDFObject
from Probabilistic.Parameter import ParameterType, ProbabilisticParameter

class Building(IDFObject.IDFObject):
    __IDFName__ = "Building"
    
    Properties = [
        'Name',
        'NorthAxis',
        'Terrain',
        'LoadConvergenceTolerance',
        'TemperatureConvergenceTolerance',
        
        'SolarDistribution',

        'MaximumNumberOfWarmUpDays',
        'MinimumNumberOfWarmUpDays',
    ]

    __geometryInitialised = False
    
    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)