import re
import json

from idf_object.schedule.compact import Compact
from idf_object.scheduletypelimits import ScheduleTypeLimits

OfficeSchedules = None
def GetOfficeSchedules(file, scheduleTypeFiles):
    with open(file) as f1, open(scheduleTypeFiles) as f2:
        schedules = get_schedules(json.load(f1), json.load(f2))
    return schedules

def get_schedules(schedules_json, schedules_types_json):
    Compact.InitialiseScheduleTypes(schedules_types_json)
    objs = list()
    objs.append(ScheduleTypeLimits())
    
    for zoneList in schedules_json:
        schedules = schedules_json[zoneList]
        for schedule in schedules:
            d = schedules[schedule]
            s = Compact(Name = f'{zoneList}.{schedule}', **getattr(Compact, d['Type']))
            s.assign_keys(d)
            objs.append(s)

    return objs

def set_setpoints(parameters, ep_objects,):
    schedules = list(x for x in ep_objects if isinstance(x, Compact))
    
    for parameter in parameters.index:
        if not re.fullmatch('.*SP:.*', parameter): continue
        (schedule_name, names) = parameter.split(':')
        for name in names.split('|'):
            try:
                schedule = next(x for x in schedules if x.Name==f'Schedule.{name}.{schedule_name}')
                schedule.assign_values(v1=parameters[parameter]-4, v2=parameters[parameter])
            except StopIteration: pass

def fill_schedules(ep_objects):
    schedules = list(x for x in ep_objects if isinstance(x, Compact))
    for schedule in schedules:
        schedule.assign_values(t1='07:30', t2='17:00', t3='13:00')
        schedule_type = schedule.Name.split('.')[-1]
        if schedule_type == 'People': schedule.assign_values(v1=0, v2=1)
        elif schedule_type == 'Activity': schedule.assign_values(v1=140)
        elif schedule_type == 'Lights' or schedule_type == 'ElectricEquipment': schedule.assign_values(v1=0.1, v2=1)
        elif schedule_type == 'HeatingSP': schedule.assign_values(v1=16, v2=20)
        elif schedule_type == 'CoolingSP': schedule.assign_values(v1=30, v2=26)