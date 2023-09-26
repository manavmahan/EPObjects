from idf_object import IDFObject
    
class Shade(IDFObject):
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
        'LeftSideOpeningMultiplier',
        'RightSideOpeningMultiplier',
        'AirflowPermeability',
    ]

    default = dict(Name = 'RollShade',
        SolarTransmittance = 0.3,
        SolarReflectance = 0.5,
        VisibleTransmittance = 0.3,
        VisibleReflectance = 0.5,
        InfraredHemisphericalEmissivity = 0.9,
        InfraredTransmittance = 0.05,
        Thickness = 0.003,
        Conductivity = 0.1,
        ShadetoGlassDistance = 0.05,
        TopOpeningMultiplier = 0,
        BottomOpeningMultiplier = 0.5,
        LeftSideOpeningMultiplier = 0.5,
        RightSideOpeningMultiplier = 0,
        AirflowPermeability = '',
    )
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)