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

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)

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