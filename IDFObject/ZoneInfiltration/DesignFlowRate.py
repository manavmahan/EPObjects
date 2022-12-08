from IDFObject import IDFObject
    
class DesignFlowRate(IDFObject.IDFObject):
    __IDFName__ = 'ZoneInfiltration:DesignFlowRate'
    Properties = [
        'Name',
        'ZoneListName',
        'ScheduleName',
        'DesignFlowRateCalculationMethod',
        'DesignFlowRate',
        'FlowperZoneFloorArea',
        'FlowperExteriorSurfaceArea',
        'AirChangesperHour',
        'ConstantTermCoefficient',
        'TemperatureTermCoefficient',
        'VelocityTermCoefficient',
        'VelocitySquaredTermCoefficient',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

DesignFlowRate.Default = dict(
    DesignFlowRateCalculationMethod = 'AirChanges/Hour',
    
)