from IDFObject.IDFObject import IDFObject
    
class VariableFlow(IDFObject):
    __IDFName__ = 'ZoneHVAC:LowTemperatureRadiant:VariableFlow'
    Properties = [
        'Name',
        'DesignObjectName',
        'AvailabilityScheduleName',
        'ZoneName',
        'SurfaceNameorRadiantSurfaceGroupName',
        'HydronicTubingLength',
        'HeatingDesignCapacity',
        'MaximumHotWaterFlow',
        'HeatingWaterInletNodeName',
        'HeatingWaterOutletNodeName',
        'CoolingDesignCapacity',
        'MaximumColdWaterFlow',
        'CoolingWaterInletNodeName',
        'CoolingWaterOutletNodeName',
        'NumberofCircuits',
        'CircuitLength',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

VariableFlow.Default = dict(
    AvailabilityScheduleName='Always1',
    HydronicTubingLength='Autosize',
    HeatingDesignCapacity='Autosize',
    MaximumHotWaterFlow='Autosize',
    HeatingWaterInletNodeName='Heating Coil Load Loop Supply Outlet Node',
    HeatingWaterOutletNodeName='Heating Coil Load Loop Intermediate Node',
    CoolingDesignCapacity='Autosize',
    MaximumColdWaterFlow='Autosize',
    CoolingWaterInletNodeName='',
    CoolingWaterOutletNodeName='',
    NumberofCircuits=' ',
    CircuitLength=''
)
