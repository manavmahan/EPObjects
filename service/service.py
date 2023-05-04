user_name = "manav"
project_name = "tausendpfund"
DB_URL = "http://127.0.0.1:3000/api/db/"

from service import json, pd, np, os, requests

from IDFObject.IDFObject import IDFJsonDecoder
from Probabilistic.EnergyPredictions import ProbabilisticEnergyPrediction
from Probabilistic.Parameter import ProbabilisticParameters

from service.energy_model_simulations import generate_simulation_results, get_run_periods
from service.train_ml_networks import train_generator, train_regressor

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
    consumption_df = pd.DataFrame.from_dict(json.loads(project_data["CONSUMPTION"]),)
    parameters_df = pd.DataFrame.from_dict(json.loads(project_data["PARAMETERS"]))

    _, consumption = get_run_periods(consumption_df)

    project_settings = {
        "SIMULATE": False,
        "REGRESSOR": False,
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
            "ENERGY_SYSTEM": "Heat Pumps",
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
    
    regressor_targets = ProbabilisticEnergyPrediction.from_json(json.loads(response['RESULTS'][0]["SIMULATION_RESULTS"])).Values["Total"]
    sampled_parameters = pd.DataFrame.from_dict(json.loads(response['RESULTS'][0]["SAMPLED_PARAMETERS"]))

    if project_settings["REGRESSOR"]:
        network, loss = train_regressor(user_name, project_name, ProbabilisticParameters.from_df(parameters_df), sampled_parameters, regressor_targets)
        data = {
            "TYPE": "UPDATE_ITEM", 
            "TABLE_NAME": "PROJECTS",
            "SET_VALUES": f"REGRESSOR='[{network},{json.dumps(loss)}]'",
            "CONDITIONS": project_search_conditions,
        }

        response = requests.post(DB_URL, json=data).json()
        if (response["ERROR"]):
            raise ValueError(response["ERROR"])
    

    if project_settings["GENERATOR"]:
        data = {
            "TYPE": "SEARCH", 
            "TABLE_NAME": "PROJECTS",
            "COLUMN_NAMES": "REGRESSOR",
            "CONDITIONS": project_search_conditions,
        }
        response = requests.post(DB_URL, json=data).json()
        if (response["ERROR"]):
            raise ValueError(response["ERROR"])
        
        regressor_json = json.dumps(json.loads(response["RESULTS"][0]["REGRESSOR"])[0])
        generators = train_generator(   user_name,
                                        project_name,
                                        ProbabilisticParameters.from_df(parameters_df),
                                        regressor_json, 
                                        consumption)
        for (network, loss) in generators:
            data = {
                "TYPE": "SEARCH", 
                "TABLE_NAME": "PROJECTS",
                "COLUMN_NAMES": "GENERATORS",
                "CONDITIONS": project_search_conditions,
            }

            response = requests.post(DB_URL, json=data).json()
            if (response["ERROR"]):
                raise ValueError(response["ERROR"])
            
            if len(response["RESULTS"]) == 0:
                generators = []
            else:
                try:
                    generators = json.loads(response["RESULTS"][0]["GENERATORS"])
                except TypeError:
                    generators = []

            generators += (f'({network}, {loss})')
            data = {
                "TYPE": "UPDATE_ITEM", 
                "TABLE_NAME": "PROJECTS",
                "SET_VALUES": f"GENERATORS='[{network},{json.dumps(loss)}]'",
                "CONDITIONS": project_search_conditions,
            }
            

