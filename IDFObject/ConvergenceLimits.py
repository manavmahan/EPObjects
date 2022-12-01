from IDFObject import IDFObject
    
class ConvergenceLimits(IDFObject.IDFObject):
    __IDFName__ = 'ConvergenceLimits'
    Properties = [
        'MinimumSystemTimestep',
        'MaximumHVACIterations',
        'MinimumPlantIterations',
        'MaximumPlantIterations',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
