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

    def ChangeValues(self, values):
        for key in values:
            self.Fields = self.Fields.replace(key, str(values[key]))
    
    @staticmethod
    def GetCompactSchedule(data):
        s = Compact(getattr(Compact, data['Type']))
        s.ChangeValues(data)

Compact.HeatingCoolingSeason = dict(
    Name = 'HeatingCoolingSeason',
    ScheduleTypeLimitsName = ScheduleTypeLimits.AnyNumber['Name'],
    Fields = '''
        Through: 5/23,
            For: Alldays,
                Until: 24:00,1,
        Through: 7/30,
            For: Alldays,
                Until: 24:00,2,
        Through: 12/31,
            For: Alldays,
                Until: 24:00,1'
    '''
)

Compact.FourAndHalfDays = dict(
    ScheduleTypeLimitsName = ScheduleTypeLimits.AnyNumber['Name'],
    Fields = f'''
        Through 12/31, 
            For: Mondays Tuesdays Wednesday Thursdays SummerDesignDay WinterDesignDay CustomDay1 CustomDay2,
                Until: t1, v1, Until: t2, v2, Until: 24:00, v1,
            For: Fridays,
                Until: t1, v1, Until: t3, v2, Until: 24:00, v1,
            For: Weekends Holidays,
                Until: 24:00, v1
    '''
)

Compact.SingleValue = dict(
    ScheduleTypeLimitsName = ScheduleTypeLimits.AnyNumber['Name'],
    Fields = f'''
        Through 12/31, 
            For: Alldays,
                Until: 24:00, v1
    '''
)