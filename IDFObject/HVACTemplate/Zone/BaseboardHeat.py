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

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
    
    @classmethod
    def get_default(cls, **kwargs):
        props = dict(BaseboardHeat.Default)
        props.update(kwargs)
        return BaseboardHeat(props)

BaseboardHeat.Default = dict(
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
