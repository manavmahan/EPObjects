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

    def ChangeValues(values):


Compact.HeatingCoolingSeason = dict(
    Name = 'HeatingCoolingSeason',
    ScheduleTypeLimitsName = ScheduleTypeLimits.AnyNumber['Name'],
    Fields = 'Through: 5/23,For: Alldays,Until: 24:00,1,Through: 7/30,For: Alldays,Until: 24:00,2,Through: 12/31,For: Alldays,Until: 24:00,1',
)

Compact.OfficePeople = dict(
    Name = 'People.Office',
    ScheduleTypeLimitsName = ScheduleTypeLimits.AnyNumber['Name'],
    Fields = f'Through 12/31, For: Mondays Tuesdays Wednesday Thursdays, Until: 07:30, value0, '
)