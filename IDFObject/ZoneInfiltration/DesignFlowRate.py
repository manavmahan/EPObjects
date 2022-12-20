from IDFObject.IDFObject import IDFObject

class DesignFlowRate(IDFObject):
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
    ScheduleName = "Always1",
    DesignFlowRateCalculationMethod = 'AirChanges/Hour',
    DesignFlowRate = '',
    FlowperZoneFloorArea = '',
    FlowperExteriorSurfaceArea = '',
    AirChangesperHour = 0.31,
    ConstantTermCoefficient = 0.606,
    TemperatureTermCoefficient = 0.03636,
    VelocityTermCoefficient = 0.1177165,
    VelocitySquaredTermCoefficient = '',
)