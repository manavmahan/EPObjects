from IDFObject import IDFObject
    
class InternalMass(IDFObject.IDFObject):
    __IDFName__ = 'InternalMass'
    Properties = [
        'Name',
        'ConstructionName',
        'ZoneName',
        'SurfaceArea',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

InternalMass.Default = dict(
    ConstructionName = "Mass",
)