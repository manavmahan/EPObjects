import pandas as pd
from datetime import datetime

from idf_object.runperiod import RunPeriod

def get_run_periods(df):
    periods = []
    for m, row in df.iterrows():
        begin_date = datetime.strptime(row['BeginDate'], '%Y-%m-%d')
        end_date = datetime.strptime(row['EndDate'], '%Y-%m-%d')
        r = RunPeriod(
            Name = f'RunPeriod{m}',
            BeginYear = begin_date.year, EndYear = end_date.year,
            BeginMonth = begin_date.month, EndMonth = end_date.month,
            BeginDayofMonth = begin_date.day, EndDayofMonth = end_date.day,
        )
        periods += [r]
    
    return periods, df[[v for v in df.columns if 'value' in v]]

def get_run_periods_from_file(file):
    df = pd.read_csv(file, index_col=0)
    return get_run_periods(df)