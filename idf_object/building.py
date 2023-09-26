import numpy as np

from idf_object import IDFObject
from probabilistic.parameter import ParameterType, ProbabilisticParameter

class Building(IDFObject):
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
    
    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
