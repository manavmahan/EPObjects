from IDFObject.IDFObject import IDFObject
    
class HotWaterLoop(IDFObject):
    __IDFName__ = 'HVACTemplate:Plant:HotWaterLoop'
    Properties = [
        'PlantLoopName',
        'PumpSchedule',
        'PumpControlType',
        'HotWaterPlantOperationSchemeType',
        'HotWaterPlantOperationSchemeListName',
        'HotWaterSetpointSchedule',
        'HotWaterDesignSetpoint',
        'HotWaterPumpConfiguration',
        'HotWaterPumpRatedHead',
        'HotWaterSetpointResetType',
        'HotWaterSetpointatOutdoorDryBulbLow',
        'HotWaterResetOutdoorDryBulbLow',
        'HotWaterSetpointatOutdoorDryBulbHigh',
        'HotWaterResetOutdoorDryBulbHigh',
        'HotWaterPumpType',
        'SupplySideBypassPipe',
        'DemandSideBypassPipe',
        'FluidType',
        'LoopDesignDeltaTemperature',
        'MaximumOutdoorDryBulbTemperature',
        'LoadDistributionScheme',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

    @classmethod
    def get_default(cls, **kwargs):
        props = dict(HotWaterLoop.Default)
        props.update(kwargs)
        return HotWaterLoop(props)

HotWaterLoop.Default = dict(
    PlantLoopName = 'HotWaterLoop',
    PumpSchedule = ' ',
    PumpControlType = 'Intermittent',
    HotWaterPlantOperationSchemeType = 'Default',
    HotWaterPlantOperationSchemeListName = ' ',
    HotWaterSetpointSchedule = 'HWLoopTempSchedule',
    HotWaterDesignSetpoint = '82',
    HotWaterPumpConfiguration = 'VariableFlow',
    HotWaterPumpRatedHead = '179352',
    HotWaterSetpointResetType = 'None',
    HotWaterSetpointatOutdoorDryBulbLow = '82.2',
    HotWaterResetOutdoorDryBulbLow = '-6.7',
    HotWaterSetpointatOutdoorDryBulbHigh = '65.6',
    HotWaterResetOutdoorDryBulbHigh = '10',
    HotWaterPumpType = 'SinglePump',
    SupplySideBypassPipe = 'Yes',
    DemandSideBypassPipe = 'Yes',
    FluidType = 'Water',
    LoopDesignDeltaTemperature = '11',
    MaximumOutdoorDryBulbTemperature = ' ',
    LoadDistributionScheme = 'Sequential'
)
