from IDFObject import IDFObject
    
class Lights(IDFObject.IDFObject):
    __IDFName__ = 'Lights'
    Properties = [
        'Name',
        'ZoneorZoneListName',
        'ScheduleName',
        'DesignLevelCalculationMethod',
        'LightingLevel',
        'WattsperZoneFloorArea',
        'WattsperPerson',
        'ReturnAirFraction',
        'FractionRadiant',
        'FractionVisible',
        'FractionReplaceable',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
