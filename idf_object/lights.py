from idf_object import IDFObject
    
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

    default = dict(
        DesignLevelCalculationMethod = 'Watts/area',
        LightingLevel = '',
        WattsperZoneFloorArea = 6,
        WattsperPerson = '',
        ReturnAirFraction = '',
        FractionRadiant = 0.1,
        FractionVisible = 0.18,
        FractionReplaceable = '',
    )

    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
