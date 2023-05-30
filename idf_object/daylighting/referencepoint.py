from idf_object import IDFObject
import numpy as np
    
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
        self.Point = np.round(self.Point, 5)
