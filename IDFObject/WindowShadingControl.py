from IDFObject import IDFObject
    
class WindowShadingControl(IDFObject.IDFObject):
    __IDFName__ = 'WindowShadingControl'
    Properties = [
        'Name',
        'ZoneName',
        'ShadingControlSequenceNumber',
        'ShadingType',
        'ConstructionwithShadingName',
        'ShadingControlType',
        'ScheduleName',
        'Setpoint',
        'ShadingControlIsScheduled',
        'GlareControlIsActive',
        'ShadingDeviceMaterialName',
        'TypeofSlatAngleControlforBlinds',
        'SlatAngleScheduleName',
        'Setpoint',
        'DaylightingControlObjectName',
        'MultipleSurfaceControlType',
        'FenestrationSurfaceName',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

WindowShadingControl.Default = dict(
    ShadingControlSequenceNumber = '',
    ShadingType = "InteriorShade",
    ConstructionwithShadingName = '',
    ShadingControlType = "OnIfHighZoneAirTemperature",
    ScheduleName = '',
    Setpoint = 23,
    ShadingControlIsScheduled = "NO",
    GlareControlIsActive = "NO",
    ShadingDeviceMaterialName = "ROLLSHADE",
    TypeofSlatAngleControlforBlinds = '',
    SlatAngleScheduleName = '',
    MultipleSurfaceControlType = '',
)