from IDFObject.IDFObject import IDFObject
    
class Heating(IDFObject):
    __IDFName__ = 'HeatPump:PlantLoop:EIR:Heating'
    Properties = [
        'Name',
        'LoadSideInletNodeName',
        'LoadSideOutletNodeName',
        'CondenserType',
        'SourceSideInletNodeName',
        'SourceSideOutletNodeName',
        'CompanionHeatPumpName',
        'LoadSideDesignVolumeFlowRate',
        'SourceSideDesignVolumeFlowRate',
        'ReferenceCapacity',
        'ReferenceCOP',
        'SizingFactor',
        'HPHeatingCAPFTemp',
        'HPHeatingEIRFTemp',
        'HPHeatPLFFPLR',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

Heating.Default = dict(
    Name = 'Heating Coil',
    LoadSideInletNodeName = 'Heating Coil Load Loop Intermediate Node',
    LoadSideOutletNodeName = 'Heating Coil Load Loop Supply Outlet Node',
    CondenserType = 'AirSource',
    SourceSideInletNodeName = 'Outdoor Air HP Inlet Node',
    SourceSideOutletNodeName = 'Outdoor Air HP Outlet Node',
    CompanionHeatPumpName = '',
    LoadSideDesignVolumeFlowRate = 0.005,
    SourceSideDesignVolumeFlowRate = 0.002,
    ReferenceCapacity = 45000,
    ReferenceCOP = 3.5,
    SizingFactor = '',
    HeatingCapacityModifierFunctionofTemperatureCurveName = '',
    ElectricInputtoHeatingOutputRatioModifierFunctionofTemperatureCurveName = '',
    ElectricInputtoHeatingOutputRatioModifierFunctionofPartLoadRatioCurveName = '',
)
