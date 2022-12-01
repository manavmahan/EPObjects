from IDFObject import IDFObject
    
class ElectricEquipment(IDFObject.IDFObject):
    __IDFName__ = 'ElectricEquipment'
    Properties = [
        'Name',
        'ZoneorZoneListName',
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
