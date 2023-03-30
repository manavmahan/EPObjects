import json

from Helper.Modules import *

from pathlib import Path
Home = str(Path.home())

RepoPath = f'{Home}/repos/EPObjects/Tausendpfund/'

with open(f'{RepoPath}/Geometry.json') as f:
    epObjects = json.load(f, cls=IDFJsonDecoder)

with open(f'{RepoPath}/Geometry-wIDFName.json', 'w') as f:
   json.dump(epObjects, f, cls=IDFJsonEncoder, indent=4)