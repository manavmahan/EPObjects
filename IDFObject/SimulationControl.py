from IDFObject import IDFObject
    
class SimulationControl(IDFObject.IDFObject):
    __IDFName__ = 'SimulationControl'
    Properties = [
        'DoZoneSizingCalculation',
        'DoSystemSizingCalculation',
        'DoPlantSizingCalculationRun',
        'SimulationforSizingPeriods',
        'RunSimulationforSizingPeriods',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
