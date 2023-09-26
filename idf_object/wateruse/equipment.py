from idf_object import IDFObject

class Equipment(IDFObject):
    __IDFName__ = 'WaterUse:Equipment'
    Properties = [
        "Name",
        "EndUseSubcategory",
        "PeakFlowRate",
        "FlowRateFractionScheduleName",
        "TargetTemperatureScheduleName",
        "HotWaterSupplyTemperatureScheduleName",
        "ColdWaterSupplyTemperatureScheduleName",
    ]

    default = dict(
        Name = 'HotWater',
        EndUseSubcategory = 'DomesticHotWater',
        PeakFlowRate = '0.001',
        FlowRateFractionScheduleName = 'HotWaterSchedule',
        TargetTemperatureScheduleName = 'Always45',
        HotWaterSupplyTemperatureScheduleName = 'Always60',
        ColdWaterSupplyTemperatureScheduleName = ''
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
