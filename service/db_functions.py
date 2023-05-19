from service import json, JsonDecoder, JsonEncoder, pd, requests, DB_URL, HEADER

BUILDING_USE = "BUILDING_USE"
CONSUMPTION = "CONSUMPTION"
ERRORS = "ERRORS"
GEOMETRY = "GEOMETRY"
GENERATIVE = "GENERATIVE"
GENERATORS = "GENERATORS"
GENERATOR_SETTINGS = "GENERATOR_SETTINGS"
HYPERPARAMETERS = "HYPERPARAMETERS"
INVERTED = "INVERTED"
LOCATION = "LOCATION"
LOSS = "LOSS"
METHOD = "METHOD"
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
    return f"PROJECT_NAME='{project_name}' AND USER_NAME='{user_name}'"

def get_columns(search_conditions: str, column_name: str, convert_to_df=False):
    """ Retrieves the selected columns from the DB. """
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "PROJECTS",
        "COLUMN_NAMES": column_name,
        "CONDITIONS": search_conditions,
    }
    response = requests.post(DB_URL, headers=HEADER, json=data).json()
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

    response = requests.post(DB_URL, headers=HEADER, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])

def get_weather(location):
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "WEATHER",
        "COLUMN_NAMES": "EPW_STR",
        "CONDITIONS": f"LOCATION='{location}'",
    }
    response = requests.post(DB_URL, headers=HEADER, json=data).json()
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

    response = requests.post(DB_URL, headers=HEADER, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find SETTINGS for {building_use}.")
    return response["RESULTS"][0]["SETTINGS"]

def get_zonelist_settings(building_use, zonelist_name):
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "zonelist",
        "COLUMN_NAMES": "value",
        "CONDITIONS": f"buildingUse='{building_use}' and name='{zonelist_name}'",
    }

    response = requests.post(DB_URL, headers=HEADER, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find SETTINGS for {building_use} and {zonelist_name}.")
    value = json.loads(response["RESULTS"][0]["value"], cls=JsonDecoder)
    return value

def get_hyperparameters(search_conditions=True, regressor=True, generator=True):
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "REGRESSOR_HYPERPARAMETERS" if regressor else "GENERATOR_HYPERPARAMETERS" if generator else None,
        "COLUMN_NAMES": "VALUE",
        "CONDITIONS": search_conditions,
    }
    response = requests.post(DB_URL, headers=HEADER, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find SETTINGS for {search_conditions}.")
    
    value = json.loads(response["RESULTS"][0]["VALUE"], cls=JsonDecoder)
    return value

def get_regressor_hyperparameters(search_conditions=True):
    return get_hyperparameters(search_conditions, regressor=True)

def get_genertor_hyperparameters(search_conditions=True):
    return get_hyperparameters(search_conditions, generator=True)

def get_auxiliary_objects(search_conditions=True):
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "auxiliaryObjects",
        "COLUMN_NAMES": "value",
        "CONDITIONS": search_conditions,
    }
    response = requests.post(DB_URL, headers=HEADER, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find SETTINGS for {search_conditions}.")
    
    for obj in response["RESULTS"]:
        yield json.loads(obj["value"], cls=JsonDecoder)

def get_construction_material(names, is_construction=True):
    search_condition = f"name='{names[0]}'"
    for name in names[1:]:
        search_condition += f"|'{name}'"
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "constructions" if is_construction else 'materials',
        "COLUMN_NAMES": "value",
        "CONDITIONS": search_condition,
    }
    response = requests.post(DB_URL, headers=HEADER, json=data).json()
    if (response["ERROR"]):
        raise ValueError(response["ERROR"])
    if len(response["RESULTS"]) == 0:
        raise ValueError(f"Cannot find construction for {name}.")
    
    for obj in response["RESULTS"]:
        yield json.loads(obj["value"], cls=JsonDecoder)