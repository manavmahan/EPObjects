import pandas as pd

from Helper.Modules import RunPeriod

def get_run_periods(df):
    periods = []
    for m, row in df.iterrows():
        r = RunPeriod(
            Name = f'RunPeriod{m}',
            BeginYear = int(row['BeginYear']), EndYear = int(row['EndYear']),
            BeginMonth = int(row['BeginMonth']), EndMonth = int(row['EndMonth']),
            BeginDayofMonth = int(row['BeginDay']), EndDayofMonth = int(row['EndDay']),
        )
        periods += [r]
    
    return periods, df[[v for v in df.columns if 'value' in v]]

def get_run_periods_from_file(file):
    df = pd.read_csv(file, index_col=0)
    return get_run_periods(df)