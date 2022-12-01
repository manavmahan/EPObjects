from IDFObject import IDFObject
    
class SimpleGlazingSystem(IDFObject.IDFObject):
    __IDFName__ = 'WindowMaterial:SimpleGlazingSystem'
    Properties = [
        'Name',
        'U-Factor',
        'SolarHeatGainCoefficient',
        'VisibleTransmittance',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
