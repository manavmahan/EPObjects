from IDFObject.IDFObject import IDFObject
    
class ElectricEquipment(IDFObject):
    __IDFName__ = 'ElectricEquipment'
    Properties = [
        'Name',
        'ZoneListName',
        'ScheduleName',
        'DesignLevelCalculationMethod',
        'DesignLevel',
        'WattsperZoneFloorArea',
        'WattsperPerson',
        'FractionLatent',
        'FractionRadiant',
        'FractionLost',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

ElectricEquipment.Default = dict(
    DesignLevelCalculationMethod = 'Watts/area',
    DesignLevel = '',
    WattsperZoneFloorArea = 10,
    WattsperPerson = '',
    FractionLatent = '',
    FractionRadiant = 0.1,
    FractionLost = '',
)