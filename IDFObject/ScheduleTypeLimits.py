from IDFObject.IDFObject import IDFObject
    
class ScheduleTypeLimits(IDFObject):
    __IDFName__ = 'ScheduleTypeLimits'
    Properties = [
        'Name',
        'Fields',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

ScheduleTypeLimits.AnyNumber = dict(
    Name = "Any Number",
    Fields = '',
)