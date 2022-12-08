from IDFObject.IDFObject import IDFObject
    
class SimpleGlazingSystem(IDFObject):
    __IDFName__ = 'WindowMaterial:SimpleGlazingSystem'
    Properties = [
        'Name',
        'UFactor',
        'SolarHeatGainCoefficient',
        'VisibleTransmittance',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
