from idf_object import IDFObject
    
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

    default = dict(
        DesignLevelCalculationMethod = 'Watts/area',
        DesignLevel = '',
        WattsperZoneFloorArea = 10,
        WattsperPerson = '',
        FractionLatent = '',
        FractionRadiant = 0.1,
        FractionLost = '',
    )

    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)