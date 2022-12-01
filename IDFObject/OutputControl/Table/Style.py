from IDFObject import IDFObject
    
class Style(IDFObject.IDFObject):
    __IDFName__ = 'OutputControl:Table:Style'
    Properties = [
        'ColumnSeparator',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
