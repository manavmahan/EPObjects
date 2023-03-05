from bs4 import BeautifulSoup

from datetime import date, datetime, timedelta 
import pandas as pd
import numpy as np

import urllib.request

from IDFObject.Schedule.File import File as ScheduleFile

Days = np.array([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
def GetKnownHolidays(year: int, location='Munich'):
    address = f'https://leaveboard.com/public-holidays/germany-bavaria-public-holidays-{year}/'
    contents = BeautifulSoup(urllib.request.urlopen(address).read(), "html.parser")
    holidays = []
    for holiday in contents.body.find_all('span', attrs={'class':'float-right d-none d-md-inline'}):
        day = datetime.strptime(holiday.text, "%A %B %d, %Y")
        holidays += [day.day + Days[:day.month].sum() - 1]
    return np.array(holidays)

def GetSpecificDay(year: int, day: int):
    firstDay = date(year, 1, 1)
    while firstDay.weekday() != day:
        firstDay += timedelta(days=1)
    return np.arange(firstDay.day-1, 365, 7)

def GetWeekend(year: int):
    return np.concatenate((GetSpecificDay(year, 5), GetSpecificDay(year, 6)))

def GetWorkingDays(year: int):
    workingDays = np.ones(365)
    workingDays[GetKnownHolidays(year)] = 0
    workingDays[GetWeekend(year)] = 0
    return workingDays.reshape(-1, 1)

def GetOnOff(workingDays, hours1, hours2):
    day = np.array( [0] * hours1 + [1] * (hours2 - hours1) + [0] * (24 - hours2) ).reshape(1, -1)
    return (workingDays * day).reshape(-1)

def CreateZoneListSchedule(year, zonelistName, variables):
    workingDays = GetWorkingDays(year)
    vacationHours = GetVacationHours()
    heatingCoolingSeason = GetHeatingCoolingSeason()

    columns = []
    for schedule in variables:
        sch = GetOnOff(workingDays, variables[schedule]['Hour1'], variables[schedule]['Hour2'])
        if 'Heating' in schedule: sch = sch * heatingCoolingSeason[0]
        if 'Cooling' in schedule: sch = sch * heatingCoolingSeason[1]

        column = pd.Series([variables[schedule]['Value'][int(x)] for x in sch], name=f'{zonelistName}.{schedule}')
        if 'People' in schedule: column = column * vacationHours

        IncreaseHeatingSetpoints(column, 'Heating', [5, 8, 9], 2)
        IncreaseHeatingSetpoints(column, 'Heating', [0, 1, 11], -2)
        columns += [column]
    return columns

def IncreaseHeatingSetpoints(column, key, months, increase=2):
    if not key in column.name: return
    for month in months: column[sum(Days[:month]) * 24 : sum(Days[:month+1]) * 24] += increase

def CreateOfficeSchedule(year, zonelists, file):
    cols = []
    for zl in zonelists:
        cols += CreateZoneListSchedule(year, zl, zonelists[zl])

    cols += GetHeatingCoolingSeason()
    
    dfs = pd.concat(cols, axis=1,)
    dfs.to_csv(file, index=False)
    for i, c in enumerate(dfs.columns):
        d = dict(ScheduleFile.Default)
        d.update(dict(
            Name = c,
            NameofFile = file,
            ColumnNumber = i+1, 
        ))
        yield ScheduleFile(d)

def GetHeatingCoolingSeason():
    heating = (
        (0, sum(Days[:5])),            # cooling from the last week of May
        (sum(Days[:9]), sum(Days)),    # heating from the second week of Sep
    )
    heatingSeason = np.zeros(24 * 365)
    for h in heating:
        heatingSeason[24*h[0]:24*h[1]] = 1

    coolingSeason = np.abs(heatingSeason - np.ones_like(heatingSeason))
    return pd.Series(heatingSeason, name="HeatingSeason"), pd.Seies(coolingSeason, name="CoolingSeason")

def GetVacationHours():
    # design days: Jan 06-12, Apr 05-11, Jul 13-19, Aug 10-16, Oct 20-26, Dec 08-14
    vacations = (
        (0, 7, 0.25),
        (7, 14, 0.5),                                  
        (sum(Days[:4]) +  7, sum(Days[:4]) + 14, 0.5), 
        (sum(Days[:5]) + 17, sum(Days[:4]) + 31, 0.5), 
        (sum(Days[:6]) + 16, sum(Days[:6]) + 30, 0.5), 
        (sum(Days[:7]) + 20, sum(Days[:7]) + 27, 0.5), 
        (sum(Days[:8]) + 17, sum(Days[:8]) + 24, 0.5), 
        (sum(Days[:9]) + 21, sum(Days[:9]) + 28, 0.5), 
        (sum(Days[:12])+ 17,sum(Days[:12]) + 24, 0.5), 
        (sum(Days[:12])+ 24,sum(Days[:12]) + 31, 0.25)
    )
    vacationHours = np.ones(24 * 365)
    for vacation in vacations:
        vacationHours[24*vacation[0]:24*vacation[1]] = vacation[2]
    return vacationHours

DefaultOfficeSchedules = dict(
    Office = dict(
        HeatingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (15, 21),
        ),

        CoolingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (30, 24),
        ),

        ElectricEquipment = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        Lights = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        People = dict(
            Hour1 = 8,
            Hour2 = 17,
            Value = (0, 1),
        ),

        Activity = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (140, 140),
        ),
    ),
    Stairs = dict(
        HeatingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (15, 21),
        ),

        CoolingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (30, 24),
        ),

        ElectricEquipment = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        Lights = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        People = dict(
            Hour1 = 8,
            Hour2 = 17,
            Value = (0, 1),
        ),

        Activity = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (200, 200),
        ),
    ),
    Toilet = dict(
        HeatingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (15, 21),
        ),

        CoolingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (30, 24),
        ),

        ElectricEquipment = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        Lights = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        People = dict(
            Hour1 = 8,
            Hour2 = 17,
            Value = (0, 1),
        ),

        Activity = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (200, 200),
        ),
    ),
    Service = dict(
        HeatingSetPoint = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (0, 0),
        ),

        CoolingSetPoint = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (20, 20),
        ),

        ElectricEquipment = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (1, 1),
        ),

        Lights = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        People = dict(
            Hour1 = 7,
            Hour2 = 20,
            Value = (0, 0),
        ),

        Activity = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (200, 200),
        ),
    ),

    Corridor = dict(
        HeatingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (15, 21),
        ),

        CoolingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (30, 24),
        ),

        ElectricEquipment = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        Lights = dict(
            Hour1 = 7,
            Hour2 = 17,
            Value = (0.1, 1),
        ),

        People = dict(
            Hour1 = 8,
            Hour2 = 17,
            Value = (0, 1),
        ),

        Activity = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (200, 200),
        ),
    ),

    Technic = dict(
        HeatingSetPoint = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (0, 0),
        ),

        CoolingSetPoint = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (35, 35),
        ),

        ElectricEquipment = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (1, 1),
        ),

        Lights = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (1, 1),
        ),

        People = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (0, 0),
        ),

        Activity = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (200, 200),
        ),
    )
)