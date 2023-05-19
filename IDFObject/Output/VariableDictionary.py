from IDFObject import IDFObject
    
class VariableDictionary(IDFObject.IDFObject):
    __IDFName__ = 'Output:VariableDictionary'
    Properties = [
        'KeyField',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
