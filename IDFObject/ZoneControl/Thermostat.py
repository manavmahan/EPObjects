from IDFObject.IDFObject import IDFObject
    
class Thermostat(IDFObject):
    __IDFName__ = 'ZoneControl:Thermostat'
    Properties = [
        'Name',
        'ZoneorZoneListName',
        'ControlTypeScheduleName',
        'Control1ObjectType',
        'Control1Name',
        'Control2ObjectType',
        'Control2Name',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

Thermostat.Default = dict(
    Control1ObjectType = 'ThermostatSetpoint:SingleHeating',
    Control2ObjectType = 'ThermostatSetpoint:SingleCooling',
)
