from service import json, pd, DB_URL, requests, create_simulation_dir, JsonEncoder
import service.db_functions as db

from IDFObject.IDFObject import IDFJsonDecoder
from Probabilistic.EnergyPredictions import ProbabilisticEnergyPrediction
from Probabilistic.Parameter import ProbabilisticParameters

from service.energy_model_simulations import generate_simulation_results, get_run_periods
from service.train_ml_networks import train_generator, train_regressor

def run_service(user_name, project_name):
    info = f'User: {user_name}\tProject: {project_name}\t'
    search_conditions = db.get_search_conditions(user_name, project_name)

    project_settings = {
        "BUILDING_USE": "OFFICE",
        "LOCATION": "Regensburg, Germany",

        "SIMULATION_SETTINGS": {
            "SIMULATE": False,
            "NUM_SAMPLES": 40,
            "ENERGY_SYSTEM": "Heat Pumps",
            "HOT_WATER": False,
            "INTERNAL_SHADING": True,
            "SIMULATION_DEFAULTS": {
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
            },
        },
        "REGRESSOR_SETTINGS":{
            "TRAIN": False,
        },
        "GENERATOR_SETTINGS": {
            "TRAIN": True,
        }
    }

    if project_settings[db.SIMULATION_SETTINGS]["SIMULATE"]:
        epw_str = db.get_weather(project_settings[db.LOCATION])
        idf_folder = create_simulation_dir(user_name, project_name, epw_str)
        geometry_json = db.get_columns(search_conditions, db.GEOMETRY,)
        schedules_json = db.get_columns(search_conditions, db.SCHEDULES)
        consumption_df = pd.DataFrame.from_dict(db.get_columns(search_conditions, db.CONSUMPTION),)
        parameters_df = pd.DataFrame.from_dict(db.get_columns(search_conditions, db.PARAMETERS),)

        sampled_parameters, simulation_results = generate_simulation_results(
            info, idf_folder,
            project_settings[db.SIMULATION_SETTINGS], 
            geometry_json, schedules_json,
            parameters_df, consumption_df,
        )
        db.update_columns(search_conditions, 
                          (db.SIMULATION_RESULTS, simulation_results),
                          (db.SAMPLED_PARAMETERS, sampled_parameters))
    
    
    if project_settings[db.REGRESSOR_SETTINGS][db.TRAIN]:
        sampled_parameters_json = db.get_columns(search_conditions, db.SAMPLED_PARAMETERS)
        simulation_results_json = db.get_columns(search_conditions, db.SIMULATION_RESULTS)
        parameters_df = pd.DataFrame.from_dict(db.get_columns(search_conditions, db.PARAMETERS),)
        parameters = ProbabilisticParameters.from_df(parameters_df)

        regressor_targets = ProbabilisticEnergyPrediction.from_json(simulation_results_json).Values["Total"]
        sampled_parameters = pd.DataFrame.from_dict(sampled_parameters_json)
        parameters = ProbabilisticParameters.from_df(parameters_df)

        network, loss = train_regressor(info, parameters, sampled_parameters, regressor_targets)
        db.update_columns(search_conditions, db.REGRESSOR, {db.NETWORK: network, db.LOSS: loss},)

    if project_settings[db.GENERATOR_SETTINGS][db.TRAIN]:
        regressor = db.get_columns(search_conditions, db.REGRESSOR)[db.NETWORK]
        
        consumption_df = pd.DataFrame.from_dict(db.get_columns(search_conditions, db.CONSUMPTION),)
        _, consumption = get_run_periods(consumption_df)

        parameters_df = pd.DataFrame.from_dict(db.get_columns(search_conditions, db.PARAMETERS),)
        parameters = ProbabilisticParameters.from_df(parameters_df)
        generators = train_generator(   info,
                                        parameters,
                                        regressor, 
                                        consumption)
        db.update_columns(search_conditions, db.GENERATORS, None)
        for (network, loss) in generators:
            generators = db.get_columns(search_conditions, db.GENERATORS)
            if generators == None:
                generators = {db.NETWORK: [], db.LOSS: []}

            generators[db.NETWORK] += [network]
            generators[db.LOSS] +=  [loss]

            db.update_columns(search_conditions, db.GENERATORS, generators)