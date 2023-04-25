user_name = "manav"
project_name = "tausendpfund"
DB_URL = "http://127.0.0.1:3001/"

from service import json, pd, np, os, requests

from IDFObject.IDFObject import IDFJsonDecoder
from Probabilistic.EnergyPredictions import ProbabilisticEnergyPrediction

from service.energy_model_simulations import generate_simulation_results

def run_service(user_name, project_name):
    project_search_conditions = f"PROJECT_NAME='{project_name}' AND USER_NAME='{user_name}'"
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "PROJECTS",
        "COLUMN_NAMES": "GEOMETRY,SCHEDULES,CONSUMPTION,PARAMETERS",
        "CONDITIONS": project_search_conditions,
    }

    response = requests.post(DB_URL, json=data).json()
    if (response["ERROR"] or len(response['RESULTS'])==0):
        raise ValueError("Cannot get project from the database!")

    project_data = response['RESULTS'][0]
    geometry_json = json.loads(project_data["GEOMETRY"], cls=IDFJsonDecoder)
    schedules_json = json.loads(project_data["SCHEDULES"])
    consumption_df = pd.DataFrame.from_dict(json.loads(project_data["CONSUMPTION"]))
    parameters_df = pd.DataFrame.from_dict(json.loads(project_data["PARAMETERS"]))

    project_settings = {
        "SIMULATE": False,
        "REGRESSOR": True,
        "GENERATOR": True,
        "LOCATION": "Regensburg, Germany"
    }

    if project_settings["SIMULATE"]:
        simulation_settings = {
            "NUM_SAMPLES": 40,
        }

        office_simulation_defaults = {
            "ZONE": {
                "INTERNAL_MASS": 25,
                "INFILTRATION": 0.3,
            },

            "ZONELISTS":{
                "Office": dict(People = 24.0, Lights = 6.0, Equipment = 15,),
                "Toilet": dict(People = 48.0, Lights = 4.5, Equipment = 5,),
                "Stairs": dict(People = 48.0, Lights = 4.5, Equipment = 5,),
                "Corridor": dict(People = 48.0, Lights = 4.5, Equipment = 10,),
                "Service": dict(People = 100.0, Lights = 1.0, Equipment = 25,),
                "Technic": dict(People = 100.0, Lights = 1.0, Equipment = 10,),
            }
        }

        project_simulation_model_settings = {
            "ENERGY_SYSTEM": "HeatPump",
            "HOT_WATER": False,
            "INTERNAL_SHADING": True,

        }

        location = project_settings["LOCATION"]
        data = {
            "TYPE": "SEARCH", 
            "TABLE_NAME": "WEATHER",
            "COLUMN_NAMES": "EPW_STR",
            "CONDITIONS": f"LOCATION='{location}'",
        }

        response = requests.post(DB_URL, json=data).json()
        if (response["ERROR"] or len(response['RESULTS'])==0):
            print (response["QUERY"])
            raise ValueError("Cannot get weather data from the database!")

        epw_str = response['RESULTS'][0]["EPW_STR"]

        sampled_parameters, simulation_results = generate_simulation_results(user_name, project_name, 
                                    epw_str,
                                    simulation_settings, 
                                    geometry_json, 
                                    schedules_json, 
                                    office_simulation_defaults, 
                                    project_simulation_model_settings,
                                    parameters_df,
                                    consumption_df,)
        data = {
            "TYPE": "UPDATE_ITEM", 
            "TABLE_NAME": "PROJECTS",
            "SET_VALUES": f"SIMULATION_RESULTS='{simulation_results}',SAMPLED_PARAMETERS='{sampled_parameters}'",
            "CONDITIONS": project_search_conditions,
        }

        response = requests.post(DB_URL, json=data).json()
        if (response["ERROR"]):
            raise ValueError(response["ERROR"])
    
    data = {
        "TYPE": "SEARCH", 
        "TABLE_NAME": "PROJECTS",
        "COLUMN_NAMES": "SAMPLED_PARAMETERS,SIMULATION_RESULTS",
        "CONDITIONS": project_search_conditions,
    }

    response = requests.post(DB_URL, json=data).json()
    if (response["ERROR"] or len(response['RESULTS'])==0):
        raise ValueError("Cannot get project from the database!")
    
    print (ProbabilisticEnergyPrediction.from_json(json.loads(response['RESULTS'][0]["SIMULATION_RESULTS"])))
    print (pd.DataFrame.from_dict(json.loads(response['RESULTS'][0]["SAMPLED_PARAMETERS"])).head(20))