import numpy as np

from IDFObject import IDFObject

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
    
    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
