from service import np, pd, create_simulation_dir, logger
import service.db_functions as db

from Probabilistic.EnergyPredictions import ProbabilisticEnergyPrediction
from Probabilistic.Parameter import ProbabilisticParameters

from service.energy_model_simulations import generate_simulation_results, get_run_periods
from service.ml_networks import train_generator, train_regressor, predict

def run_service(user_name, project_name):
    info = f'User: {user_name}\tProject: {project_name}\t'
    search_conditions = db.get_search_conditions(user_name, project_name)

    project_settings = {
        "BUILDING_USE": "OFFICE",
        "LOCATION": "Regensburg, Germany",

        "SIMULATION_SETTINGS": {
            "RUN": True,
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
            "RUN": True,
        },
        "GENERATOR_SETTINGS": {
            "RUN": True,
        },
        "RESULTS":{
            "RUN": True,
            "NUM_SAMPLES": 50,
            "NUM_SAMPLES_PER_GENERATOR": 3,
        }
    }

    if project_settings[db.SIMULATION_SETTINGS][db.RUN]:
        epw_str = db.get_weather(project_settings[db.LOCATION])
        idf_folder = create_simulation_dir(user_name, project_name, epw_str)
        geometry_json = db.get_columns(search_conditions, db.GEOMETRY,)
        schedules_json = db.get_columns(search_conditions, db.SCHEDULES)
        consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)

        sampled_parameters, simulation_results = generate_simulation_results(
            info, idf_folder,
            project_settings[db.SIMULATION_SETTINGS], 
            geometry_json, schedules_json,
            parameters_df, consumption_df,
        )
        db.update_columns(search_conditions, db.SIMULATION_RESULTS, simulation_results)
        db.update_columns(search_conditions, db.SAMPLED_PARAMETERS, sampled_parameters)

    if project_settings[db.REGRESSOR_SETTINGS][db.RUN]:
        sampled_parameters = db.get_columns(search_conditions, db.SAMPLED_PARAMETERS, True)
        simulation_results = db.get_columns(search_conditions, db.SIMULATION_RESULTS,)
        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
        parameters = ProbabilisticParameters.from_df(parameters_df)

        regressor_targets = ProbabilisticEnergyPrediction.from_json(simulation_results).Values["Total"]

        network, loss = train_regressor(info, parameters, sampled_parameters, regressor_targets)
        db.update_columns(search_conditions, db.REGRESSOR, {db.NETWORK: network, db.LOSS: loss},)

    if project_settings[db.GENERATOR_SETTINGS][db.RUN]:
        regressor = db.get_columns(search_conditions, db.REGRESSOR)[db.NETWORK]
        
        consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
        _, consumption = get_run_periods(consumption_df)

        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
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

            i = 0
            while len(generators[db.LOSS]) > i and loss < generators[db.LOSS][i]:
                i += 1
            generators[db.NETWORK].insert(i, network)
            generators[db.LOSS].insert(i, loss)
            db.update_columns(search_conditions, db.GENERATORS, generators)

    if project_settings[db.RESULTS][db.RUN]:
        num_samples = project_settings[db.RESULTS]["NUM_SAMPLES"]
        num_samples_per_generator = project_settings[db.RESULTS]["NUM_SAMPLES_PER_GENERATOR"]
        generators = db.get_columns(search_conditions, db.GENERATORS)[db.NETWORK]
        regressor = db.get_columns(search_conditions, db.REGRESSOR)[db.NETWORK]

        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
        consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
        _, consumption = get_run_periods(consumption_df)
        m_consumption = consumption.mean(axis=1).values.T
        total_consumption = m_consumption.sum()

        results = pd.DataFrame(columns = parameters_df.index)
 
        for i in range(num_samples):
            if i >= len (generators):
                logger.info(info, f"NUM_SAMPLES {num_samples} more than {len(generators)}")
                break
            p_parameters = predict(generators[i], num_examples = num_samples_per_generator)
            m = i * num_samples_per_generator
            for p in range(num_samples_per_generator):
                results.loc[f'p_{m+p}'] = p_parameters[p]

        results[consumption_df["Name"]] = predict(regressor, X=results[parameters_df.index])
        results['Total'] = results[consumption_df["Name"]].sum(axis=1)
        results[[f'Error_{x}' for x in consumption_df["Name"]]] = (results[consumption_df["Name"]].values - m_consumption) / m_consumption
        results['Error'] = (results['Total']-total_consumption) / total_consumption
        
        print (results)
        db.update_columns(search_conditions, db.RESULTS, results)
