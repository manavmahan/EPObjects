import re

regex = re.compile(r"{.*.}")

lines = '''Schedule:File,
  elecTDVfromCZ01res, !- Name
  Any Number,         !- ScheduleType
  TDV_kBtu_CTZ01csv, !- Name of File
  2,                  !- Column Number
  4,                  !- Rows to Skip at Top
  8760,               !- Number of Hours of Data
  Comma;              !- Column Separator'''.split('\n')

fileName = lines[0].replace(',', '')
columnNames = [ regex.sub("", x[x.index('!- ')+3:]).replace(' ', '').replace('\t', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('!- ')].replace(' ', '').replace(',','').replace('\t', '') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

with open(f'Data/{fileName}.txt', 'w') as f:
    f.write(','.join(columnNames) + '\n' + ','.join(values))