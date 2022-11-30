import pandas as pd

from IDFObject import IDFObject

class Material(IDFObject.IDFObject):
    __IDFName__ = 'Material'
    Properties = [
        'Name',
        'Thickness',
        'Conductivity',
        'Density',
        'Specific Heat',
        'Thermal Absorptance',
        'Solar Absorptance',
        'Visible Absorptance',
    ]

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)

    def __eq__(self, other):
        return self.Name == other.Name

    def __lt__(self, other):
        return self.Name < other.Name