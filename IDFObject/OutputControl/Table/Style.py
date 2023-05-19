from IDFObject import IDFObject
    
class Style(IDFObject.IDFObject):
    __IDFName__ = 'OutputControl:Table:Style'
    Properties = [
        'ColumnSeparator',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
