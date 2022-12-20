from GeometryObject.XYZ import XYZ
from IDFObject.IDFObject import IDFObject
    
class ReferencePoint(IDFObject):
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
        self.Point = XYZ(self.Point)
