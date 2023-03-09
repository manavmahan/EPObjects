from IDFObject.IDFObject import IDFObject
    
class Cooling(IDFObject):
    __IDFName__ = 'HeatPump:WaterToWater:EIR:Cooling'
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
'HeatingCapacityModifierFunctionofTemperatureCurveName',
'ElectricInputtoHeatingOutputRatioModifierFunctionofTemperatureCurveName',
'ElectricInputtoHeatingOutputRatioModifierFunctionofPartLoadRatioCurveName',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
