from GeometryObject import XYZ
from IDFObject import IDFObject
    
class ReferencePoint(IDFObject.IDFObject):
    __IDFName__ = 'Daylighting:ReferencePoint'
    Properties = [
        'Name',
        'ZoneName',
        'Point',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        self.Initialise()

    def Initialise(self):
        self.Point = XYZ.XYZ(self.Point)
