from IDFObject import IDFObject
    
class ScheduleTypeLimits(IDFObject.IDFObject):
    __IDFName__ = 'ScheduleTypeLimits'
    Properties = [
        'Name',
        'LowerLimitValue',
        'UpperLimitValue',
        'NumericType',
        'UnitType',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
