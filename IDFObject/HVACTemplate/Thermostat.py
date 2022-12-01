from IDFObject import IDFObject
    
class Thermostat(IDFObject.IDFObject):
    __IDFName__ = 'HVACTemplate:Thermostat'
    Properties = [
        'Name',
        'HeatingSetpointScheduleName',
        'ConstantHeatingSetpoint',
        'CoolingSetpointScheduleName',
        'ConstantCoolingSetpoint',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
