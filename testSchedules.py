from IDFObject.Schedule.Compact import Compact

from Helper.ScheduleHelper import GetOfficeSchedules

Compact.InitialiseScheduleTypes("Tausendpfund/ScheduleTypes.json")

epObjects = GetOfficeSchedules()
print ([list(x.ToDict()) for x in epObjects])