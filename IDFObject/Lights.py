from IDFObject.IDFObject import IDFObject
    
class Lights(IDFObject):
    __IDFName__ = 'Lights'
    Properties = [
        'Name',
        'ZoneListName',
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

Lights.Default = dict(
    ScheduleName = 'Office.Lights',
    DesignLevelCalculationMethod = 'Watts/area',
    LightingLevel = '',
    WattsperZoneFloorArea = 7,
    WattsperPerson = '',
    ReturnAirFraction = '',
    FractionRadiant = 0.1,
    FractionVisible = 0.18,
    FractionReplaceable = '',
)