import re

regex = re.compile(r"{.*.}")

lines = '''Site:Precipitation,
  ScheduledAndDesignLevel, !- Precipitation Model Type
  0.75,                    !- Design Level Total Annual Precipitation
  PrecipitationSchd,       !- Schedule Name for Precipitation Rates
  0.80771;                 !- Average Total Annual Precipitation'''.split('\n')

fileName = lines[0].replace(',', '')
columnNames = [ regex.sub("", x[x.index('!-')+3:]).replace(' ', '').replace('\t', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('!-')].replace(' ', '').replace(',','').replace('\t', '') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

with open(f'Data/{fileName}.txt', 'w') as f:
    f.write(','.join(columnNames) + '\n' + ','.join(values))