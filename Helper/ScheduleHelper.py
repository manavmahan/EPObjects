import re
import json

from IDFObject.Schedule.Compact import Compact
from IDFObject.ScheduleTypeLimits import ScheduleTypeLimits

OfficeSchedules = None
def GetOfficeSchedules(file, scheduleTypeFiles):
    with open(file) as f1, open(scheduleTypeFiles) as f2:
        schedules = get_schedules(json.load(f1), json.load(f2))
    return schedules

def get_schedules(schedules_json, schedules_types_json):
    Compact.InitialiseScheduleTypes(schedules_types_json)
    objs = list()
    objs.append(ScheduleTypeLimits(ScheduleTypeLimits.AnyNumber))
    
    for zoneList in schedules_json:
        schedules = schedules_json[zoneList]
        for schedule in schedules:
            d = schedules[schedule]
            s = Compact(getattr(Compact, d['Type']))
            s.Name = f'{zoneList}.{schedule}'
            s.ChangeValues(d)
            objs.append(s)

    return objs

def SetBestMatchSetpoints(probabilisticParameters, epObjects, defaultSchedules):
    schedules = list(x for x in epObjects if isinstance(x, Compact))
    
    for parameter in probabilisticParameters.index:
        if not re.fullmatch('.*Set.*point.*', parameter): continue
        (scheduleName, names) = parameter.split(':')
        for name in names.split('|'):
            try:
                schedule = next(x for x in schedules if x.Name==f'{name}.{scheduleName}')
                epObjects.remove(schedule)
            except StopIteration: pass

            d = defaultSchedules[name][scheduleName]
            d['<v2>'] = probabilisticParameters[parameter]
            s = Compact(getattr(Compact, d['Type']))
            s.Name = f'{name}.{scheduleName}'
            s.ChangeValues(d)
            epObjects.append(s)
