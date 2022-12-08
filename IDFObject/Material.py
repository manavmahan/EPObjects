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

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)

    def __eq__(self, other):
        return self.Name == other.Name

    def __lt__(self, other):
        return self.Name < other.Name