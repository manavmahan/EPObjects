from IDFObject import IDFObject
    
class BuildingSurface(IDFObject.IDFObject):
    __IDFName__ = 'Site:GroundTemperature:BuildingSurface'
    Properties = [
        'JanuaryGroundTemperature',
        'FebruaryGroundTemperature',
        'MarchGroundTemperature',
        'AprilGroundTemperature',
        'MayGroundTemperature',
        'JuneGroundTemperature',
        'JulyGroundTemperature',
        'AugustGroundTemperature',
        'SeptemberGroundTemperature',
        'OctoberGroundTemperature',
        'NovemberGroundTemperature',
        'DecemberGroundTemperature',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
