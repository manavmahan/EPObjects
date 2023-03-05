import pandas as pd

from Helper.Modules import RunPeriod
from Helper.ScheduleHelper import Days

def SetRunPeriod(months=range(1, 13), year=2017):
    for m in months:
        r = RunPeriod(RunPeriod.Default)
        r.Name = f'RunPeriod{m}'
        r.BeginYear, r.EndYear = year, year
        r.BeginMonth, r.EndMonth = m, m
        r.EndDayofMonth = Days[m-1]
        yield r

def GetRunPeriodsFromFile(file):
    df = pd.read_csv(file)

    periods = []
    for m, row in df.iterrows():
        r = RunPeriod(RunPeriod.Default)
        r.Name = f'RunPeriod{m}'
        r.BeginYear, r.EndYear = row['BeginYear'], row['EndYear']
        r.BeginMonth, r.EndMonth = row['BeginYear'], row['EndYear']
        r.BeginDayofMonth, r.EndDayofMonth = row['BeginDayofMonth'], row['EndDayofMonth']
        periods += [r]
    
    return periods, df['Values']