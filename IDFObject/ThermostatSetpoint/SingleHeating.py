from IDFObject.IDFObject import IDFObject
    
class SingleHeating(IDFObject):
    __IDFName__ = 'ThermostatSetpoint:SingleHeating'
    Properties = [
        'Name',
        'SetpointTemperatureScheduleName',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
