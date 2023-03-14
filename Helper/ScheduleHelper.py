import re
from IDFObject.Schedule.Compact import Compact
from IDFObject.ScheduleTypeLimits import ScheduleTypeLimits

DefaultOfficeSchedules = dict(
    Generic = dict(
        Always1 = dict(
            Type = 'SingleValue',
            v1 = 1,
        ),

        Always01 = dict(
            Type = 'SingleValue',
            v1 = 0.1,
        ),
    ),

    Office = dict(
        HeatingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 15,
            v2 = 20,
        ),
        CoolingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 30,
            v2 = 25,
        ),
        ElectricEquipment = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        Lights = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        People = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.0,
            v2 = 1.0,
        ),
        Activity = dict(
            Type = 'SingleValue',
            v1 = 140,
        ),
    ),

    Stairs = dict(
        HeatingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 15,
            v2 = 20,
        ),
        CoolingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 30,
            v2 = 25,
        ),
        ElectricEquipment = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        Lights = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        People = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.0,
            v2 = 1.0,
        ),
        Activity = dict(
            Type = 'SingleValue',
            v1 = 140,
        ),
    ),

    Toilet = dict(
        HeatingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 15,
            v2 = 20,
        ),
        CoolingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 30,
            v2 = 25,
        ),
        ElectricEquipment = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        Lights = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        People = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.0,
            v2 = 1.0,
        ),
        Activity = dict(
            Type = 'SingleValue',
            v1 = 140,
        ),
    ),

    Service = dict(
        HeatingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 15,
            v2 = 20,
        ),
        CoolingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 30,
            v2 = 25,
        ),
        ElectricEquipment = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        Lights = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        People = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.0,
            v2 = 1.0,
        ),
        Activity = dict(
            Type = 'SingleValue',
            v1 = 140,
        ),
    ),

    Corridor = dict(
        HeatingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 15,
            v2 = 20,
        ),
        CoolingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 30,
            v2 = 25,
        ),
        ElectricEquipment = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        Lights = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        People = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.0,
            v2 = 1.0,
        ),
        Activity = dict(
            Type = 'SingleValue',
            v1 = 140,
        ),
    ),

    Technic = dict(
        HeatingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 15,
            v2 = 20,
        ),
        CoolingSetpoint = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:00',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 30,
            v2 = 25,
        ),
        ElectricEquipment = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        Lights = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.1,
            v2 = 1.0,
        ),
        People = dict(
            Type = 'FourAndHalfDays',
            t1 = '07:30',
            t2 = '17:00',
            t3 = '13:00',
            v1 = 0.0,
            v2 = 1.0,
        ),
        Activity = dict(
            Type = 'SingleValue',
            v1 = 140,
        ),
    )
)

def GetOfficeSchedules():
    objs = list()
    objs.append(ScheduleTypeLimits(ScheduleTypeLimits.AnyNumber))

    for zoneList in DefaultOfficeSchedules:
        schedules = DefaultOfficeSchedules[zoneList]
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
            except: pass

            d = DefaultOfficeSchedules[name][scheduleName]
            d['v2'] = probabilisticParameters[parameter]
            s = Compact(getattr(Compact, d['Type']))
            s.Name = f'{name}.{scheduleName}'
            s.ChangeValues(d)
            epObjects.append(s)
