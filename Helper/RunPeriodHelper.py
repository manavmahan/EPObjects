import pandas as pd

from Helper.Modules import RunPeriod

def get_run_periods(df):
    periods = []
    for m, row in df.iterrows():
        r = RunPeriod(RunPeriod.Default)
        r.Name = f'RunPeriod{m}'
        r.BeginYear, r.EndYear = int(row['BeginYear']), int(row['EndYear'])
        r.BeginMonth, r.EndMonth = int(row['BeginMonth']), int(row['EndMonth'])
        r.BeginDayofMonth, r.EndDayofMonth = int(row['BeginDay']), int(row['EndDay'])
        periods += [r]
    
    return periods, df[[v for v in df.columns if 'value' in v]]

def get_run_periods_from_file(file):
    df = pd.read_csv(file, index_col=0)
    return get_run_periods(df)