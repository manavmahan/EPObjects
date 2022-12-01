from IDFObject import IDFObject
    
class Shade(IDFObject.IDFObject):
    __IDFName__ = 'WindowMaterial:Shade'
    Properties = [
        'Name',
        'SolarTransmittance',
        'SolarReflectance',
        'VisibleTransmittance',
        'VisibleReflectance',
        'InfraredHemisphericalEmissivity',
        'InfraredTransmittance',
        'Thickness',
        'Conductivity',
        'ShadetoGlassDistance',
        'TopOpeningMultiplier',
        'BottomOpeningMultiplier',
        'Left-SideOpeningMultiplier',
        'Right-SideOpeningMultiplier',
        'AirflowPermeability',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
