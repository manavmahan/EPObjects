import json

from IDFObject.IDFObject import IDFObject
from IDFObject.ScheduleTypeLimits import ScheduleTypeLimits
    
class Compact(IDFObject):
    __IDFName__ = 'Schedule:Compact'
    Properties = [
        'Name',
        'ScheduleTypeLimitsName',
        'Fields',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        if isinstance(self.Fields, list):
            self.Fields = '\n'.join(self.Fields)

    def ChangeValues(self, values):
        for key in values:
            self.Fields = self.Fields.replace(key, str(values[key]))

    @classmethod
    def InitialiseScheduleTypes(cls, data):
        for x in data:
            setattr(Compact, x["Type"], x)
    
    @classmethod
    def GetCompactSchedule(cls, data):
        s = Compact(getattr(Compact, data['Type']))
        s.ChangeValues(data)