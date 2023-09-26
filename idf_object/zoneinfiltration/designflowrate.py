from idf_object import IDFObject

class DesignFlowRate(IDFObject):
    __IDFName__ = 'ZoneInfiltration:DesignFlowRate'
    Properties = [
        'Name',
        'ZoneListName',
        'ScheduleName',
        'DesignFlowRateCalculationMethod',
        'DesignFlowRate',
        'FlowperZoneFloorArea',
        'FlowperExteriorSurfaceArea',
        'AirChangesperHour',
        'ConstantTermCoefficient',
        'TemperatureTermCoefficient',
        'VelocityTermCoefficient',
        'VelocitySquaredTermCoefficient',
    ]

    default = dict(
        ScheduleName = "Generic.Always1",
        DesignFlowRateCalculationMethod = 'AirChanges/Hour',
        DesignFlowRate = '',
        FlowperZoneFloorArea = '',
        FlowperExteriorSurfaceArea = '',
        AirChangesperHour = 0.31,
        ConstantTermCoefficient = 0.606,
        TemperatureTermCoefficient = 0.03636,
        VelocityTermCoefficient = 0.1177165,
        VelocitySquaredTermCoefficient = '',
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)