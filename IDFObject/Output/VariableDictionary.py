from IDFObject import IDFObject
    
class VariableDictionary(IDFObject.IDFObject):
    __IDFName__ = 'Output:VariableDictionary'
    Properties = [
        'KeyField',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
