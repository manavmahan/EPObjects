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
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)


    def __eq__(self, other):
        return self.Name == other.Name

    def __lt__(self, other):
        return self.Name < other.Name