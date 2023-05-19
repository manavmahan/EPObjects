from IDFObject.IDFObject import IDFObject
    
class ScheduleTypeLimits(IDFObject):
    __IDFName__ = 'ScheduleTypeLimits'
    Properties = [
        'Name',
        'Fields',
    ]

    default = dict(
        Name = "Any Number",
        Fields = '',
    )
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)


ScheduleTypeLimits.AnyNumber = dict(
    Name = "Any Number",
    Fields = '',
)