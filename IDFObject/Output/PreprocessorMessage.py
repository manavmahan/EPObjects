from IDFObject import IDFObject
    
class PreprocessorMessage(IDFObject.IDFObject):
    __IDFName__ = 'Output:PreprocessorMessage'
    Properties = [
        'PreprocessorName',
        'ErrorSeverity',
        'MessageLine1',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
