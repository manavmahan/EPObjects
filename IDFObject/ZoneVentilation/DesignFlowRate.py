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
    DesignFlowRateCalculationMethod = "Flow/Person",
    DesignFlowRate = 0,
    FlowRateperZoneFloorArea = 0,
    FlowRateperPerson = 0.00944,
    AirChangesperHour = '',
    VentilationType = "Balanced",
    FanPressureRise = 1,
    FanTotalEfficiency = 1,
    ConstantTermCoefficient = 1,
    TemperatureTermCoefficient = 0,
    VelocityTermCoefficient = 0,
    VelocitySquaredTermCoefficient = 0,
    MinimumIndoorTemperature = -100,
    MinimumIndoorTemperatureSchedule = '',
    MaximumIndoorTemperature = 100,
    MaximumIndoorTemperatureSchedule = '' ,
    DeltaTemperature = 1,
)

DesignFlowRate.Minimal = dict(
    DesignFlowRateCalculationMethod = "AirChanges/Hour",
    DesignFlowRate = 0,
    FlowRateperZoneFloorArea = 0,
    FlowRateperPerson = 0,
    AirChangesperHour = 0.05,
    VentilationType = "Balanced",
    FanPressureRise = 1,
    FanTotalEfficiency = 1,
    ConstantTermCoefficient = 1,
    TemperatureTermCoefficient = 0,
    VelocityTermCoefficient = 0,
    VelocitySquaredTermCoefficient = 0,
    MinimumIndoorTemperature = -100,
    MinimumIndoorTemperatureSchedule = '',
    MaximumIndoorTemperature = 100,
    MaximumIndoorTemperatureSchedule = '' ,
    DeltaTemperature = 1,
)

DesignFlowRate.Natural = dict(
    DesignFlowRateCalculationMethod = "AirChanges/Hour",
    DesignFlowRate = 0,
    FlowRateperZoneFloorArea = 0,
    FlowRateperPerson = 0,
    AirChangesperHour = 1,
    VentilationType = "Natural",
    FanPressureRise = 0,
    FanTotalEfficiency = 0.1,
    ConstantTermCoefficient = 1,
    TemperatureTermCoefficient = 0,
    VelocityTermCoefficient = 0,
    VelocitySquaredTermCoefficient = 0,
    MinimumIndoorTemperature = 22,
    MinimumIndoorTemperatureSchedule = '',
    MaximumIndoorTemperature = 23.9,
    MaximumIndoorTemperatureSchedule = '' ,
    DeltaTemperature = 1,
)