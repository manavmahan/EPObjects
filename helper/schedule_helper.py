import re
import json

from idf_object.schedule.compact import Compact

def set_setpoints(parameters, ep_objects,):
    schedules = list(x for x in ep_objects if isinstance(x, Compact))
    for parameter in parameters.index:
        if not re.fullmatch('HeatingSP', parameter): continue
        for x in schedules:
            if parameter in x.Name:
                x.set_setpoints(parameters[parameter])

def fill_schedules(parameters, ep_objects):
    schedules = list(x for x in ep_objects if isinstance(x, Compact))
    for parameter in parameters.index:
        if not re.fullmatch('.*WeeklyHours.*', parameter): continue
        for schedule in schedules:
            schedule.distribute_weekly_hours(parameters[parameter])
    
    for schedule in schedules:
        schedule.fill_default_times()