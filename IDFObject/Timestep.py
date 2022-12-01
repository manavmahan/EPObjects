from IDFObject import IDFObject
    
class Timestep(IDFObject.IDFObject):
    __IDFName__ = 'Timestep'
    Properties = [
        'NumberofTimestepsperHour',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
