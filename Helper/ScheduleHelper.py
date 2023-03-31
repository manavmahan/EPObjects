import re
import json

from IDFObject.Schedule.Compact import Compact
from IDFObject.ScheduleTypeLimits import ScheduleTypeLimits

OfficeSchedules = None
def GetOfficeSchedules(file, scheduleTypeFiles):
    
    Compact.InitialiseScheduleTypes(scheduleTypeFiles)
    objs = list()
    objs.append(ScheduleTypeLimits(ScheduleTypeLimits.AnyNumber))

    with open(file) as f:
        global OfficeSchedules
        OfficeSchedules = json.load(f)
        for zoneList in OfficeSchedules:
            schedules = OfficeSchedules[zoneList]
            for schedule in schedules:
                d = schedules[schedule]
                s = Compact(getattr(Compact, d['Type']))
                s.Name = f'{zoneList}.{schedule}'
                s.ChangeValues(d)
                objs.append(s)

    return objs

def SetBestMatchSetpoints(probabilisticParameters, epObjects):
    schedules = list(x for x in epObjects if isinstance(x, Compact))
    
    for parameter in probabilisticParameters.index:
        if not re.fullmatch('.*Set.*point.*', parameter): continue
        (scheduleName, names) = parameter.split(':')
        for name in names.split('|'):
            try:
                schedule = next(x for x in schedules if x.Name==f'{name}.{scheduleName}')
                epObjects.remove(schedule)
            except StopIteration: pass

            d = OfficeSchedules[name][scheduleName]
            d['<v2>'] = probabilisticParameters[parameter]
            d['<v1>'] = d['<v2>'] - 4
            s = Compact(getattr(Compact, d['Type']))
            s.Name = f'{name}.{scheduleName}'
            s.ChangeValues(d)
            epObjects.append(s)
