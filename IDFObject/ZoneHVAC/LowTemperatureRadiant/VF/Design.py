from IDFObject.IDFObject import IDFObject
    
class Design(IDFObject):
    __IDFName__ = 'ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design'
    Properties = [
        'Name',
        'FluidtoRadiantSurfaceHeatTransferModel',
        'HydronicTubingInsideDiameter',
        'HydronicTubingOutsideDiameter',
        'HydronicTubingConductivity',
        'TemperatureControlType',
        'SetpointControlType',
        'HeatingDesignCapacityMethod',
        'HeatingDesignCapacityPerFloorArea',
        'FractionOfAutosizedHeatingDesignCapacity',
        'HeatingControlThrottlingRange',
        'HeatingControlTemperatureScheduleName',

        'CoolingDesignCapacityMethod',
        'CoolingDesignCapacityPerFloorArea',
        'FractionofAutosizedCoolingDesignCapacity',
        'CoolingControlThrottlingRange',
        'CoolingControlTemperatureScheduleName',
        'CondensationControlType',
        'CondensationControlDewpointOffset',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

Design.Default = dict(
    FluidtoRadiantSurfaceHeatTransferModel = 'ConvectionOnly',
    HydronicTubingInsideDiameter = '0.013',
    HydronicTubingOutsideDiameter = '0.016',
    HydronicTubingConductivity = '0.35',
    TemperatureControlType = 'MeanAirTemperature',
    SetpointControlType = 'HalfFlowPower',
    HeatingDesignCapacityMethod = 'HeatingDesignCapacity',
    HeatingDesignCapacityPerFloorArea = '',
    FractionOfAutosizedHeatingDesignCapacity = '',
    HeatingControlThrottlingRange = 2,

    HeatingControlTemperatureScheduleName = '',
    CoolingControlTemperatureScheduleName = '',

    CoolingDesignCapacityMethod = 'CoolingDesignCapacity',
    CoolingDesignCapacityPerFloorArea = '',
    FractionofAutosizedCoolingDesignCapacity = '',
    CoolingControlThrottlingRange = '2.0',
    CondensationControlType = 'Off',
    CondensationControlDewpointOffset = '',
)