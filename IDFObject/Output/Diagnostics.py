from IDFObject import IDFObject
    
class Diagnostics(IDFObject.IDFObject):
    __IDFName__ = 'Output:Diagnostics'
    Properties = [
        'Keys',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.Initialise()

    def Initialise(self):
        self.Keys = self.Keys.replace(';', ',')
