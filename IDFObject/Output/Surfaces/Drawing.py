from IDFObject import IDFObject
    
class Drawing(IDFObject.IDFObject):
    __IDFName__ = 'Output:Surfaces:Drawing'
    Properties = [
        'ReportType',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
