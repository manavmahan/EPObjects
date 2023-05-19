from IDFObject.IDFObject import IDFObject
    
class WindowShadingControl(IDFObject):
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
        'FenestrationSurfaceName',
    ]

    default = dict(
        ShadingControlSequenceNumber = 1,
        ShadingType = "InteriorShade",
        ConstructionwithShadingName = '',
        ShadingControlType = "OnIfHighHorizontalSolar",
        ScheduleName = '',
        Setpoint = 30.0,
        ShadingControlIsScheduled = "NO",
        GlareControlIsActive = "NO",
        ShadingDeviceMaterialName = "ROLLSHADE",
        TypeofSlatAngleControlforBlinds = '',
        SlatAngleScheduleName = '',
        Setpoint2 = '',
        DaylightingControlObjectName = '',
        MultipleSurfaceControlType = 'Sequential',
    )
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)