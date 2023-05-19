from IDFObject.IDFObject import IDFObject
    
class SimpleGlazingSystem(IDFObject):
    __IDFName__ = 'WindowMaterial:SimpleGlazingSystem'
    Properties = [
        'Name',
        'UFactor',
        'SolarHeatGainCoefficient',
        'VisibleTransmittance',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
