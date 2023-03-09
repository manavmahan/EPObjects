import re

regex = re.compile(r"{.*.}")

lines = '''ZoneControl:Thermostat,
    Zone 3 Thermostat,       !- Name
    NORTH ZONE,              !- Zone or ZoneList Name
    Zone Control Type Sched, !- Control Type Schedule Name
    ThermostatSetpoint:SingleHeating,  !- Control 1 Object Type
    Heating Setpoint with SB,!- Control 1 Name
    ThermostatSetpoint:SingleCooling,  !- Control 2 Object Type
    Cooling Setpoint with SB;!- Control 2 Name'''.split('\n')

fileName = lines[0].replace(',', '')
columnNames = [ regex.sub("", x[x.index('!-')+3:]).replace(' ', '').replace('\t', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('!-')].replace(' ', '').replace(',','').replace('\t', '') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

with open(f'Data/{fileName}.txt', 'w') as f:
    f.write(','.join(columnNames) + '\n' + ','.join(values))