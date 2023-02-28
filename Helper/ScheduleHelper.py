from bs4 import BeautifulSoup

from datetime import date, datetime, timedelta 
import pandas as pd
import numpy as np

import urllib.request

from IDFObject.Schedule.File import File as ScheduleFile

Days = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
def GetKnownHolidays(year: int, location='Munich'):
    address = f'https://leaveboard.com/public-holidays/germany-bavaria-public-holidays-{year}/'
    contents = BeautifulSoup(urllib.request.urlopen(address).read(), "html.parser")
    holidays = []
    for holiday in contents.body.find_all('span', attrs={'class':'float-right d-none d-md-inline'}):
        day = datetime.strptime(holiday.text, "%A %B %d, %Y")
        holidays += [day.day + Days[:day.month - 1].sum() - 1]
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
    for i in np.concatenate((GetKnownHolidays(year), GetWeekend(year))):
        workingDays[i] = 0
    return workingDays.reshape(-1, 1)

def GetOnOff(workingDays, hours1, hours2):
    dayT = np.array( [0] * hours1 + [1] * (hours2 - hours1) + [0] * (24 - hours2) ).reshape(1, -1)
    return (workingDays * dayT).reshape(-1)

def CreateZoneListSchedule(year, zonelistName, variables):
    workingDays = GetWorkingDays(year)
    vacationHours = GetVacationHours()
    columns = []

    for schedule in variables:
        sch = GetOnOff(workingDays, variables[schedule]['Hour1'], variables[schedule]['Hour2'])
        column = pd.Series([variables[schedule]['Value'][int(x)] for x in sch], name=f'{zonelistName}.{schedule}')
        if any(x in schedule for x in ('ElectricEquipment', 'Lights', 'People')):
            column = column * vacationHours
        columns += [column]
    return pd.concat(columns, axis=1)

def CreateOfficeSchedule(year, zonelists, file):
    dfs = pd.concat( [CreateZoneListSchedule(year, zl, zonelists[zl]) for zl in zonelists ] )
    dfs.to_csv(file, index=False)
    for i, c in enumerate(dfs.columns):
        d = dict(ScheduleFile.Default)
        d.update(dict(
            Name = c,
            NameofFile = file,
            ColumnNumber = i+1, 
        ))
        yield ScheduleFile(d)

def GetVacationHours():
    vacations = (
        (0, 13, 0.5), # January - 50% occupancy in the first two weeks of January = 1
        (sum(Days[:3]) + 7, sum(Days[:3]) + 14, 0.5), # Easter - 50% occupancy in an Easter week = 0.5
        (sum(Days[:5]) + 16, sum(Days[:5]) + 30, 0.5), # Summer - 50% occupancy in the last two weeks of June = 1
        (sum(Days[:6]) + 10, sum(Days[:6]) + 31, 0.5), # Summer - 50% occupancy in the last three weeks of July = 1.5
        (sum(Days[:7]) + 9, sum(Days[:7]) + 24, 0.5), # Summer - 50% occupancy in two weeks of August = 1
        (sum(Days[:11]) + 24, sum(Days[:11]) + 31, 0), # Christmas - 0% occupancy in the last week of December = 1, Total vacations week = 6
    )
    vacationHours = np.ones(24 * 365)
    for vacation in vacations:
        vacationHours[24*vacation[0]:24*vacation[1]] = vacation[2]
    return vacationHours

DefaultOfficeSchedules = dict(
    Office = dict(
        HeatingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 19,
            Value = (15, 20),
        ),

        CoolingSetPoint = dict(
            Hour1 = 7,
            Hour2 = 19,
            Value = (30, 25),
        ),

        ElectricEquipment = dict(
            Hour1 = 7,
            Hour2 = 19,
            Value = (0.1, 1),
        ),

        Lights = dict(
            Hour1 = 7,
            Hour2 = 19,
            Value = (0.1, 1),
        ),

        People = dict(
            Hour1 = 7,
            Hour2 = 19,
            Value = (0, 1),
        ),

        Activity = dict(
            Hour1 = 0,
            Hour2 = 24,
            Value = (125, 125),
        ),
    )
)