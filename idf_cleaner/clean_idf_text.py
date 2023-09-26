import re
import os

RepoPath = '/home/ubuntu/repos/EPObjects'
regex = re.compile(r"{.*.}")

lines = '''Material:AirGap,
    AIRSPACE,  ! Material Name
    0.1603675;                 ! Resistance'''.split('\n')

name = lines[0].replace(',', '')
properties_values = [x.split('! ') for x in lines[1:]]
print (properties_values)
properties = [re.sub(',| |\t', '', x[1]) for x in properties_values]
values = [re.sub(',| |\t', '', x[0]) for x in properties_values]
print (properties_values, properties, values)

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