from IDFObject import IDFObject
    
class DesignFlowRate(IDFObject.IDFObject):
    __IDFName__ = 'ZoneInfiltration:DesignFlowRate'
    Properties = [
        'Name',
        'ZoneorZoneListName',
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

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
