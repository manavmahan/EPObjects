from IDFObject import IDFObject
    
class Variable(IDFObject.IDFObject):
    __IDFName__ = 'Output:Variable'
    Properties = [
        'KeyValue',
        'Name',
        'ReportingFrequency',
    ]

    default = dict(
        KeyValue = '*',
        ReportingFrequency = "RunPeriod"
    )
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)