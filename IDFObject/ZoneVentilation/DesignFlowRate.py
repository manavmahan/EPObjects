from IDFObject.IDFObject import IDFObject
    
class DesignFlowRate(IDFObject):
    __IDFName__ = 'ZoneVentilation:DesignFlowRate'
    Properties = [
        'Name',
        'ZoneListName',
        'ScheduleName',
        'DesignFlowRateCalculationMethod',
        'DesignFlowRate',
        'FlowRateperZoneFloorArea',
        'FlowRateperPerson',
        'AirChangesperHour',
        'VentilationType',
        'FanPressureRise',
        'FanTotalEfficiency',
        'ConstantTermCoefficient',
        'TemperatureTermCoefficient',
        'VelocityTermCoefficient',
        'VelocitySquaredTermCoefficient',
        'MinimumIndoorTemperature',
        'MinimumIndoorTemperatureSchedule',
        'MaximumIndoorTemperature',
        'MaximumIndoorTemperatureSchedule',
        'DeltaTemperature',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

DesignFlowRate.Default = dict(
    DesignFlowRateCalculationMethod = "AirChanges/Hour",
    DesignFlowRate = 0,
    FlowRateperZoneFloorArea = 0,
    FlowRateperPerson = 0,
    AirChangesperHour = 2,
    VentilationType = "Natural",
    FanPressureRise = 0,
    FanTotalEfficiency = 0.1,
    ConstantTermCoefficient = 1,
    TemperatureTermCoefficient = 0,
    VelocityTermCoefficient = 0,
    VelocitySquaredTermCoefficient = 0,
    MinimumIndoorTemperature = 23,
    MinimumIndoorTemperatureSchedule = '',
    MaximumIndoorTemperature = 24.9,
    MaximumIndoorTemperatureSchedule = '' ,
    DeltaTemperature = 1,
)