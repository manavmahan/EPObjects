import json
import numpy as np
import os
import pandas as pd
import requests
import shutil

from MLModels.ml_models import model_from_json, Sequential
from IDFObject.IDFObject import IDFObject, IDFJsonDecoder, IDFJsonEncoder

from logger import logger

tmp_dir = "/tmp/energy_service/"
os.makedirs(tmp_dir, exist_ok=True)

DB_URL = "https://db.manavmahan.de"
HEADER = {
    'id': os.environ.get('API_ID')
}

def create_simulation_dir(user_name: str, project_name: str, location: str,):
    idf_folder = os.path.join(tmp_dir, user_name, project_name, "IDFFolder")
    if os.path.isdir(idf_folder): shutil.rmtree(idf_folder)

    [city, country] = location.split(',')
    country = country.lstrip()
    epw_file = os.path.join('weather', f'{country[:3].upper()}_{city}.epw')
    os.makedirs(idf_folder, exist_ok=True)
    shutil.copy(epw_file, os.path.join(idf_folder, f'{country[:3].upper()}_{city}.epw'))
    return idf_folder

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Sequential,)): 
            return json.loads(obj.to_json())

        if isinstance(obj, (IDFObject)):
            return json.dumps(obj, cls=IDFJsonEncoder)
        
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            return obj.to_dict()
        
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return json.JSONEncoder.default(self, obj)

class JsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct):
        if "__IDFName__" in dct.keys():
            return json.loads(json.dumps(dct), cls=IDFJsonDecoder)
        
        if "class_name" in dct.keys() and dct.get("class_name")=="Sequential":
            return model_from_json(json.dumps(dct))
        return dct