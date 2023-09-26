from service.service import json, JsonDecoder, JsonEncoder, pd, requests

db_url = "neo4j.manavmahan.de"
headers = {'apiid': 'f76ba64860271dd9dd21867e387004d1'}

CONSUMPTION = "CONSUMPTION"
ERRORS = "ERRORS"
GEOMETRY = "GEOMETRY"
GENERATORS = "GENERATORS"
GENERATOR_SETTINGS = "GENERATOR_SETTINGS"
HYPERPARAMETERS = "HYPERPARAMETERS"
LOCATION = "LOCATION"
LOSS = "LOSS"
NETWORK = "NETWORK"
NUMS = "NUMS"
PARAMETERS = "PARAMETERS"
PREDICTIONS = "PREDICTIONS"
PROJECT_SETTINGS = "PROJECT_SETTINGS"
REGRESSOR = "REGRESSOR"
REGRESSOR_SETTINGS = "REGRESSOR_SETTINGS"
RESULTS = "RESULTS"
RUN = "RUN"
SAMPLED_PARAMETERS = "SAMPLED_PARAMETERS"
SCALING = "SCALING"
SCHEDULES = "SCHEDULES"
SIMULATION_RESULTS = "SIMULATION_RESULTS"
SIMULATION_SETTINGS = "SIMULATION_SETTINGS"
TOTAL = "TOTAL"
TOTAL_ERROR = "TOTAL_ERROR"
WEIGHTS = "WEIGHTS"


def get_search_conditions(user_name, project_name):
    return "MATCH (n: Project) {USER_NAME='%s' PROJECT_NAME: '%s' }".format(user_name, project_name,)

def get_columns(search_conditions: str, column_name: str, convert_to_df=False):
    """ Retrieves the selected columns from the DB. """
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "PROJECTS",
        "COLUMN_NAMES": column_name,
        "CONDITIONS": search_conditions,
    }
    response = requests.post(db_url, json=data).json()
    if (response["ERROR"]): raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0: return None
    if response["RESULTS"][0][column_name] == None: return None

    value = json.loads(response["RESULTS"][0][column_name], cls=JsonDecoder)
    if convert_to_df:
        return pd.DataFrame.from_dict(value)
    return value

def update_columns(search_conditions, column_name, column_value):
    data = {
        "TYPE": "UPDATE_ITEM", 
        "TABLE_NAME": "PROJECTS",
        "SET_VALUES": f"{column_name}='{json.dumps(column_value, cls=JsonEncoder)}'",
        "CONDITIONS": search_conditions,
    }

    response = requests.post(db_url, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])

def get_weather(location):
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "WEATHER",
        "COLUMN_NAMES": "EPW_STR",
        "CONDITIONS": f"LOCATION='{location}'",
    }
    response = requests.post(db_url, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find EPW_STR for {location}.")
    return response["RESULTS"][0]["EPW_STR"]

def get_default_building_use_settings(building_use):
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "BUILDING_USE",
        "COLUMN_NAMES": "SETTINGS",
        "CONDITIONS": f"NAME='{building_use}'",
    }

    response = requests.post(db_url, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find SETTINGS for {building_use}.")
    return response["RESULTS"][0]["SETTINGS"]

def get_default_zonelist_settings(building_use, zonelist_name):
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "ZONELIST",
        "COLUMN_NAMES": "SETTINGS",
        "CONDITIONS": f"BUILDING_USE='{building_use}' and NAME='{zonelist_name}'",
    }

    response = requests.post(db_url, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find SETTINGS for {building_use} and {zonelist_name}.")
    return response["RESULTS"][0]["SETTINGS"]