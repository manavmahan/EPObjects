from IDFObject import IDFObject
    
class ZoneList(IDFObject.IDFObject):
    __IDFName__ = 'ZoneList'
    Properties = [
        'Name',
        'ZoneNames',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        self.Initialise()

    def Initialise(self):
        self.ZoneNames = self.ZoneNames.replace(';', ',')
