from IDFObject.IDFObject import IDFObject
    
class BaseboardHeat(IDFObject):
    __IDFName__ = 'HVACTemplate:Zone:BaseboardHeat'
    Properties = [
        'ZoneName',
        'TemplateThermostatName',
        'ZoneHeatingSizingFactor',
        'BaseboardHeatingType',
        'BaseboardHeatingAvailabilityScheduleName',
        'BaseboardHeatingCapacity',
        'DedicatedOutdoorAirSystemName',
        'OutdoorAirMethod',
        'OutdoorAirFlowRateperPerson',
        'OutdoorAirFlowRateperZoneFloorArea',
        'OutdoorAirFlowRateperZone',
        'DesignSpecificationOutdoorAirObjectName',
        'DesignSpecificationZoneAirDistributionObjectName',
    ]

    default = dict(
        TemplateThermostatName = 'AllZones',
        ZoneHeatingSizingFactor = '',
        BaseboardHeatingType = 'HotWater',
        BaseboardHeatingAvailabilityScheduleName = '',
        BaseboardHeatingCapacity = 'Autosize',
        DedicatedOutdoorAirSystemName = '',
        OutdoorAirMethod = 'flow/person',
        OutdoorAirFlowRateperPerson = '0.00944',
        OutdoorAirFlowRateperZoneFloorArea = '0.0',
        OutdoorAirFlowRateperZone = '0.0',
        DesignSpecificationOutdoorAirObjectName = '',
        DesignSpecificationZoneAirDistributionObjectName = ''
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)