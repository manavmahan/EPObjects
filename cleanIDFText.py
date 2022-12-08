import re

regex = re.compile(r"{.*.}")

lines = '''GlobalGeometryRules,
UpperLeftCorner,						 ! - Starting Vertex Position
Counterclockwise,						 ! - Vertex Entry Direction
Relative,						 ! - Coordinate System
Relative,						 ! - Daylighting Reference Point Coordinate System
Relative;						 ! - Rectangular Surface Coordinate System'''.split('\n')

fileName = lines[0].replace(',', '')
columnNames = [ regex.sub("", x[x.index('! - ')+2:]).replace(' ', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('! - ')].replace(' ', '').replace(',','') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

with open(f'Data/{fileName}.txt', 'w') as f:
    f.write(','.join(columnNames) + '\n' + ','.join(values))