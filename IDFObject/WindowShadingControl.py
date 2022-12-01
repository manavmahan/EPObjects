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
        'Setpoint2',
        'DaylightingControlObjectName',
        'MultipleSurfaceControlType',
        'FenestrationSurface1Name',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
