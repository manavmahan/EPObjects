from IDFObject import IDFObject
    
class Compact(IDFObject.IDFObject):
    __IDFName__ = 'Schedule:Compact'
    Properties = [
        'Name',
        'ScheduleTypeLimitsName',
        'Fields',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        self.Initialise()

    def Initialise(self):
        self.Fields = self.Fields.replace(';', ',')