import re

regex = re.compile(r"{.*.}")

lines = '''Output:PreprocessorMessage,
    ExpandObjects,           !- Preprocessor Name
    Warning,                 !- Error Severity
    Preprocessor warning;  !- Message Line 1'''.split('\n')

fileName = lines[0].replace(',', '')
columnNames = [ regex.sub("", x[x.index('!-')+2:]).replace(' ', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('!-')].replace(' ', '').replace(',','') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

with open(f'Data/{fileName}.txt', 'w') as f:
    f.write(','.join(columnNames) + '\n' + ','.join(values))