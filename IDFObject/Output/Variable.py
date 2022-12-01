from IDFObject import IDFObject
    
class Variable(IDFObject.IDFObject):
    __IDFName__ = 'Output:Variable'
    Properties = [
        'KeyValue',
        'VariableName',
        'ReportingFrequency',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
