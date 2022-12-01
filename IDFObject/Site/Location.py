from IDFObject import IDFObject
    
class Location(IDFObject.IDFObject):
    __IDFName__ = 'Site:Location'
    Properties = [
        'Name',
        'Latitude',
        'Longitude',
        'TimeZone',
        'Elevation',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
