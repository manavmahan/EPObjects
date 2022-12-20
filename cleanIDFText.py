import re

regex = re.compile(r"{.*.}")

lines = '''ZoneVentilation:DesignFlowRate,
NaturalVentilation_Office,						 ! - Name
Office,						 ! - Zone or ZoneList Name
Office_VentilationSchedule,						 ! - Schedule Name
AirChanges/Hour,						 ! - Design Flow Rate Calculation Method
0,						 ! - Design Flow Rate {m3/s}
0.001,						 ! - Flow Rate per Zone Floor Area {m3/s-m2}
0.00944,						 ! - Flow Rate per Person {m3/s-person}
2,						 ! - Air Changes per Hour {1/hr}
Natural,						 ! - Ventilation Type
1,						 ! - Fan Pressure Rise {Pa}
1,						 ! - Fan Total Efficiency
1,						 ! - Constant Term Coefficient
0,						 ! - Temperature Term Coefficient
0,						 ! - Velocity Term Coefficient
0,						 ! - Velocity Squared Term Coefficient
23,						 ! - Minimum Indoor Temperature {C}
 ,						 ! - Maximum Indoor Temperature Schedule
24.9,						 ! - Maximum Indoor Temperature {C}
 ,						 ! - Maximum Indoor Temperature Schedule
1;						 ! - Delta Temperature { deltaC}'''.split('\n')

fileName = lines[0].replace(',', '')
columnNames = [ regex.sub("", x[x.index('! - ')+3:]).replace(' ', '').replace('\t', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('! - ')].replace(' ', '').replace(',','').replace('\t', '') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

with open(f'Data/{fileName}.txt', 'w') as f:
    f.write(','.join(columnNames) + '\n' + ','.join(values))