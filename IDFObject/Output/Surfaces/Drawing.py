from IDFObject import IDFObject
    
class Drawing(IDFObject.IDFObject):
    __IDFName__ = 'Output:Surfaces:Drawing'
    Properties = [
        'ReportType',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
