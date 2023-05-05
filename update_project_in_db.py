USER_NAME = "manav"
PROJECT_NAME = "tausendpfund"
DB_URL = "http://127.0.0.1:3001/"

import json
import numpy as np
import os
import pandas as pd
import requests
from pathlib import Path
HOME = str(Path.home())

with open('Tausendpfund/Geometry.json') as f:
    d = json.load(f)

data = {
    "TYPE": "UPDATE_ITEM", 
    "TABLE_NAME": "PROJECTS",
    # "COLUMN_NAMES": "GEOMETRY",
    "SET_VALUES": f"GEOMETRY='{json.dumps(d)}'",
    "CONDITIONS": f"PROJECT_NAME='{PROJECT_NAME}' AND USER_NAME='{USER_NAME}'",
}

with open('/Users/manav/repos/EPObjects/Tausendpfund/DEU_BY_Regensburg-Oberhub.107760_TMYx.epw') as f:
    d = f.read()

data = {
    "QUERY": f"insert into WEATHER (LOCATION,EPW_STR) values ('Regensburg, Germany', '{d}');",
}

response = requests.post(DB_URL, json=data)
print (response.json()["ERROR"])#['RESULTS'])