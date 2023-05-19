from IDFObject import IDFObject
    
class ConvergenceLimits(IDFObject.IDFObject):
    __IDFName__ = 'ConvergenceLimits'
    Properties = [
        'MinimumSystemTimestep',
        'MaximumHVACIterations',
        'MinimumPlantIterations',
        'MaximumPlantIterations',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
