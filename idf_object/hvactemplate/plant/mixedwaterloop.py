from idf_object import IDFObject
    
class MixedWaterLoop(IDFObject):
    __IDFName__ = 'HVACTemplate:Plant:MixedWaterLoop'
    Properties = [
        'Name',
        'PumpScheduleName',
        'PumpControlType',
        'OperationSchemeType',
        'EquipmentOperationSchemesName',
        'HighTemperatureSetpointScheduleName',
        'HighTemperatureDesignSetpoint',
        'LowTemperatureSetpointScheduleName',
        'LowTemperatureDesignSetpoint',
        'WaterPumpConfiguration',
        'WaterPumpRatedHead',
        'WaterPumpType',
        'SupplySideBypassPipe',
        'DemandSideBypassPipe',
        'FluidType',
        'LoopDesignDeltaTemperature',
        'LoadDistributionScheme',
    ]

    default = {
        "Name": "OnlyWaterLoop", 
        "PumpScheduleName": " ", 
        "PumpControlType": "Intermittent", 
        "OperationSchemeType": "Default", 
        "EquipmentOperationSchemesName": " ",
        "HighTemperatureSetpointScheduleName": " ", 
        "HighTemperatureDesignSetpoint": 34, 
        "LowTemperatureSetpointScheduleName": " ", 
        "LowTemperatureDesignSetpoint": 20, 
        "WaterPumpConfiguration": "ConstantFlow", 
        "WaterPumpRatedHead": 179352, 
        "WaterPumpType": "SinglePump", 
        "SupplySideBypassPipe": "Yes", 
        "DemandSideBypassPipe": "Yes", 
        "FluidType": "Water", 
        "LoopDesignDeltaTemperature": 6, 
        "LoadDistributionScheme": "SequentialLoad"
    }
    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
