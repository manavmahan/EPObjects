from idf_object import IDFObject
    
class SimulationControl(IDFObject):
    __IDFName__ = 'SimulationControl'
    Properties = [
        'DoZoneSizingCalculation',
        'DoSystemSizingCalculation',
        'DoPlantSizingCalculationRun',
        'SimulationforSizingPeriods',
        'RunSimulationforSizingPeriods',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
