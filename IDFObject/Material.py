import pandas as pd

from IDFObject import IDFObject

class Material(IDFObject.IDFObject):
    __IDFName__ = 'Material'
    Properties = [
        'Name',
        'Roughness',
        'Thickness',
        'Conductivity',
        'Density',
        'SpecificHeat',
        'ThermalAbsorptance',
        'SolarAbsorptance',
        'VisibleAbsorptance',
    ]

    default = dict()
    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)