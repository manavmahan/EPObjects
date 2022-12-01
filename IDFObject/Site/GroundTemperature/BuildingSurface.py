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

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
