from IDFObject import IDFObject
    
class Version(IDFObject.IDFObject):
    __IDFName__ = 'Version'
    Properties = [
        'VersionIdentifier',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
