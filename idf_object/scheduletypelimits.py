from idf_object import IDFObject
    
class ScheduleTypeLimits(IDFObject):
    __IDFName__ = 'ScheduleTypeLimits'
    Properties = [
        'Name',
        'Fields',
    ]

    default = dict(
        Name = "AnyNumber",
        Fields = '',
    )
    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)