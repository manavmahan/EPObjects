from idf_object import IDFObject

'''
HVACTemplate:Plant:HotWaterLoop,
  Hot Water Loop,          !-Plant Loop Name
  ,                        !- Pump Schedule
  Intermittent,            !- Pump Control Type
  Default,                 !- Hot Water Plant Operation Scheme Type
  ,                        !- Hot Water Plant Operation Scheme List Name
  HW Loop Temp Schedule,   !- Hot Water Setpoint Schedule
  82,                    !- Hot Water Design Setpoint {C}
  VariableFlow,          !- Hot Water Pump Configuration
  179352,                !- Hot Water Pump Rated Head {Pa}
  None,                  !- Hot Water Setpoint Reset Type
  82.2,                  !- Hot Water Setpoint at Outdoor Dry Bulb Low {C}
  -6.7,                  !- Hot Water Reset Outdoor Dry Bulb Low {C}
  65.6,                  !- Hot Water Setpoint at Outdoor Dry Bulb High {C}
  10,                    !- Hot Water Reset Outdoor Dry Bulb High {C}
  SinglePump,              !- Hot Water Pump Type
  Yes,                     !- Supply Side Bypass Pipe
  Yes,                     !- Demand Side Bypass Pipe
  Water,                   !- Fluid Type
  11,                      !- Loop Design Delta Temperature {deltaC}
  ,                        !- Maximum Outdoor Dry Bulb Temperature {C}
  SequentialLoad;              !- Load Distribution Scheme
'''

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

    default = dict(
        PlantLoopName = 'HotWaterLoop',
        PumpSchedule = ' ',
        PumpControlType = 'Intermittent',
        HotWaterPlantOperationSchemeType = 'Default',
        HotWaterPlantOperationSchemeListName = ' ',
        HotWaterSetpointSchedule = '',
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
        LoadDistributionScheme = 'SequentialLoad'
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)

