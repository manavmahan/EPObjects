#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
import importlib

import os
import pandas as pd

from IDFFile import IDFFile

def Initialise(directory):
    for root, dirs, files in os.walk(directory):
        files.sort()
        epDict = {}
        for file in files:
            epObjects = []
            if file.endswith(".txt"):
                className = ['IDFObject'] + file[:-4].split(':')
                module = importlib.import_module('.'.join(className))
                class_ = getattr(module, className[-1])
                data = pd.read_csv(os.path.join(root,file),)
                for name in data.index:
                    epObjects += [class_(data.loc[name].to_dict())]
            epDict[file[:-4]] = epObjects
        return epDict

def InitialiseObject(dir, objectType):
    className = ['IDFObject'] + objectType.split(':')
    module = importlib.import_module('.'.join(className))
    class_ = getattr(module, className[-1])

    data = pd.read_csv(os.path.join(dir, f'{objectType}.txt'),)
    for name in data.index:
        yield class_(data.loc[name].to_dict())

def InitialiserIDFFile():
    f = IDFFile()
    print (f)

if __name__ == "__main__":
    InitialiserIDFFile()