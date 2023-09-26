import re
import os

RepoPath = '/home/ubuntu/repos/EPObjects'
regex = re.compile(r"{.*.}")

lines = '''WaterUse:Equipment,
  HotWater,   !- Name
  Domestic Hot Water,   !- EndUse Subcategory
  0.001,   !- Peak Flow Rate {m3/s}
  HotWaterSchedule,   !- Flow Rate Fraction Schedule Name
  HotWaterTargetTemp,   !- Target Temperature Schedule Name
  HotWaterSuppltTemp,   !- Hot Water Supply Temperature Schedule Name
  ;   !- Cold Water Supply Temperature Schedule Name'''.split('\n')

name = lines[0].replace(',', '')
properties = [ regex.sub("", x[x.index('!-')+3:]).replace(' ', '').replace('\t', '') for x in lines[1:] ]
values = [y if y !='' else ' ' for y in [ x[:x.index('!-')].replace(' ', '').replace(',','').replace('\t', '') for x in lines[1:] ] ]
values[-1] = values[-1][:-1]

default = "dict(\n" + ",\n".join(f"{x} = '{y}'" for (x, y) in zip(properties, values)) + '\n)'

f = name.split(':')
properties = [f'"{x}",' for x in properties]
new_line = '\n'
lines = f'''from idf_object import IDFObject

class {f[-1]}(IDFObject):
    __IDFName__ = '{name}'
    Properties = [
        {new_line.join(properties)}
    ]

    default = {default}

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
'''

f = [re.sub(r'(?<!^)(?=[A-Z])', '_', x).lower() for x in f]
pyFileName = f'{RepoPath}/idf_object/{"/".join(f)}.py'
os.makedirs(os.path.dirname(pyFileName), exist_ok=True)
            
with open(pyFileName, 'w') as fileWrite:
    fileWrite.writelines(lines)