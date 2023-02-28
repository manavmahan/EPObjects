import os
import pandas as pd

RepoPath = '/home/ubuntu/repos/EPObjects'

def Automate(root, file):
    name = file[:-4]
    f = name.split(':')

    pyFileName = f'{RepoPath}/IDFObject/{"/".join(f)}.py'
    if not os.path.exists(os.path.dirname(pyFileName)): os.makedirs(os.path.dirname(pyFileName))

    if os.path.isfile(pyFileName):
        return
    
    print (pyFileName)
    df = pd.read_csv(f'{root}/{file}')
    properties = ",\n".join(f"'{x}'" for x in df.columns) + ','
    
    lines = f'''from IDFObject.IDFObject import IDFObject
    
class {f[-1]}(IDFObject):
    __IDFName__ = '{name}'
    Properties = [
        {properties}
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
'''

    with open(pyFileName, 'w') as fileWrite:
        fileWrite.writelines(lines)

    AddTest(name, f'{root}/{file}')

def AddTest(objectName, dfFileName):
    testName = f"testReadFile{objectName.replace(':', '')}"
    line = f'    def {testName}(self):'

    with open(dfFileName, 'r') as f:
        testLine = objectName + "," + f.readlines()[1].replace(';', ',')

    currentTest = f'''{line}
        self.assertEqual("{testLine};", str(self.idfObjects['{objectName}'][0]))

'''
    
    with open(f'{RepoPath}/testIDFObject.py', 'r') as f:
        lines = f.readlines()

    for i, l in enumerate(lines):
        if not l.startswith('    def testReadFile'):
            if l == "if __name__ == '__main__':\n":
                break
        else:
            if l > line: 
                break

    with open(f'{RepoPath}/tests.py', 'w') as f:
        f.writelines(lines[:i] + [currentTest] + lines[i:])

if __name__ == "__main__":
    for root, dirs, files in os.walk(f'{RepoPath}/Data'):
        files.sort()
        epDict = {}
        for file in files:
            if file.endswith(".txt"):
                Automate(root, file)