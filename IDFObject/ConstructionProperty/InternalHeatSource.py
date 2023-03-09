from IDFObject.IDFObject import IDFObject
    
class InternalHeatSource(IDFObject):
    __IDFName__ = 'ConstructionProperty:InternalHeatSource'
    Properties = [
        'Name',
        'ConstructionName',
        'ThermalSourcePresentAfterLayerNumber',
        'TemperatureCalculationRequestedAfterLayerNumber',
        'DimensionsfortheCTFCalculation',
        'TubeSpacing',
        'TwoDimensionalTemperatureCalculationPosition',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

InternalHeatSource.Floor = dict(
    ThermalSourcePresentAfterLayerNumber = '3',
    TemperatureCalculationRequestedAfterLayerNumber = '4',
    DimensionsfortheCTFCalculation = '1',
    TubeSpacing = '0.1524',
    TwoDimensionalTemperatureCalculationPosition = '0.0'
)
