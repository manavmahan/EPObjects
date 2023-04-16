import requests
import json
import pandas as pd

client = requests.session()
URL = "http://127.0.0.1:3001/"

# with open('../Tausendpfund/Geometry.json') as f:
#     geometry = json.load(f)

# consumption = pd.read_csv('../Tausendpfund/Parameters.csv', index_col=0)

# data = {
#     "TYPE": "UPDATE_ITEM", 
#     "TABLE_NAME": "PROJECTS",
#     "SET_VALUES": f"PARAMETERS='{json.dumps(consumption.to_dict())}'",
#     "CONDITIONS": "PROJECT_NAME='TAUSENDPFUND' AND USER_NAME='MANAV'"
# }

data = {
    "TYPE": "SEARCH", 
    "TABLE_NAME": "PROJECTS",
    "COLUMN_NAMES": "CONSUMPTION",
    "CONDITIONS": "PROJECT_NAME='TAUSENDPFUND' AND USER_NAME='MANAV'",
}

response = requests.post(URL, json=data)
print (pd.read_json(response.json()['RESULT'][0][0]))