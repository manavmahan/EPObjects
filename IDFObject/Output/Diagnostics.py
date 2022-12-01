from IDFObject import IDFObject
    
class Diagnostics(IDFObject.IDFObject):
    __IDFName__ = 'Output:Diagnostics'
    Properties = [
        'Keys',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        self.Initialise()

    def Initialise(self):
        self.Keys = self.Keys.replace(';', ',')
