import re

regex = re.compile(r"{.*.}")

lines = '''HVACTemplate:Plant:HotWaterLoop,
    Hot Water Loop,          !- Plant Loop Name
    ,                        !- Pump Schedule
    Intermittent,            !- Pump Control Type
    Default,                 !- Hot Water Plant Operation Scheme Type
    ,                        !- Hot Water Plant Operation Scheme List Name
    HW Loop Temp Schedule,   !- Hot Water Setpoint Schedule
    82,                    !- Hot Water Design Setpoint {C}
    VariableFlow,          !- Hot Water Pump Configuration
    179352,                !- Hot Water Pump Rated Head {Pa}
    None,                  !- Hot Water Setpoint Reset Type
    82.2,                  !- Hot Water Setpoint at Outdoor Dry Bulb Low {C}
    -6.7,                  !- Hot Water Reset Outdoor Dry Bulb Low {C}
    65.6,                  !- Hot Water Setpoint at Outdoor Dry Bulb High {C}
    10,                    !- Hot Water Reset Outdoor Dry Bulb High {C}
    SinglePump,              !- Hot Water Pump Type
    Yes,                     !- Supply Side Bypass Pipe
    Yes,                     !- Demand Side Bypass Pipe
    Water,                   !- Fluid Type
    11,                      !- Loop Design Delta Temperature {deltaC}
    ,                        !- Maximum Outdoor Dry Bulb Temperature {C}
    Sequential;              !- Load Distribution Scheme'''.split('\n')

fileName = lines[0].replace(',', '')
columnNames = [ regex.sub("", x[x.index('!-')+3:]).replace(' ', '').replace('\t', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('!-')].replace(' ', '').replace(',','').replace('\t', '') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

with open(f'Data/{fileName}.txt', 'w') as f:
    f.write(','.join(columnNames) + '\n' + ','.join(values))