from idf_object.Schedule.Compact import Compact

from helper.schedule_helper import GetOfficeSchedules

Compact.InitialiseScheduleTypes("Tausendpfund/ScheduleTypes.json")

epObjects = GetOfficeSchedules()
print ([list(x.ToDict()) for x in epObjects])