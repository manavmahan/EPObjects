from IDFObject import IDFObject
    
class MixedWaterLoop(IDFObject.IDFObject):
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

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

MixedWaterLoop.Default = {
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
