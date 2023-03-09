from IDFObject.IDFObject import IDFObject
    
class SingleCooling(IDFObject):
    __IDFName__ = 'ThermostatSetpoint:SingleCooling'
    Properties = [
        'Name',
        'SetpointTemperatureScheduleName',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)