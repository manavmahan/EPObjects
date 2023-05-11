from service import np, pd, create_simulation_dir, logger
import service.db_functions as db

from Probabilistic.EnergyPredictions import ProbabilisticEnergyPrediction
from Probabilistic.Parameter import ProbabilisticParameters

from service.energy_model_simulations import generate_simulation_results, get_run_periods
from service.ml_networks import train_generator, train_regressor, predict, get_scaling_parameters

def run_service(user_name, project_name):
    info = f'User: {user_name}\tProject: {project_name}\t'
    search_conditions = db.get_search_conditions(user_name, project_name)

    project_settings = {
        "BUILDING_USE": "OFFICE",
        "LOCATION": "Regensburg, Germany",

        "SIMULATION_SETTINGS": {
            "RUN": False,
            "NUM_SAMPLES": 120,
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
            "RUN": False,
        },
        "GENERATOR_SETTINGS": {
            "RUN": True,
        },
        "RESULTS":{
            "RUN": True,
            "NUM_SAMPLES": 50,
            "NUM_SAMPLES_PER_GENERATOR": 2,
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
        db.update_columns(search_conditions, db.REGRESSOR, {db.NETWORK: network, db.LOSS: loss, db.WEIGHTS: network.get_weights()},)
        db.update_columns(search_conditions, db.SCALING, {db.PARAMETERS: parameters.GetScalingDF(), db.PREDICTIONS: get_scaling_parameters(regressor_targets, all_columns_equal=True)},)

    if project_settings[db.GENERATOR_SETTINGS][db.RUN]:
        regressor_data = db.get_columns(search_conditions, db.REGRESSOR)
        regressor = regressor_data[db.NETWORK]
        regressor.set_weights([np.array(x) for x in regressor_data[db.WEIGHTS]])
        
        consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
        _, consumption = get_run_periods(consumption_df)

        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
        parameters = ProbabilisticParameters.from_df(parameters_df)
        generators = train_generator(   info,
                                        parameters,
                                        regressor, 
                                        consumption)
        db.update_columns(search_conditions, db.GENERATORS, None)
        generators_data = db.get_columns(search_conditions, db.GENERATORS)
        for (network, loss) in generators:
            if generators_data == None:
                generators_data = {db.NETWORK: [], db.LOSS: [], db.WEIGHTS: []}

            i = 0
            while len(generators_data[db.LOSS]) > i and loss < generators_data[db.LOSS][i]:
                i += 1
            generators_data[db.NETWORK].insert(i, network)
            generators_data[db.LOSS].insert(i, loss)
            generators_data[db.WEIGHTS].insert(i, network.get_weights())
        db.update_columns(search_conditions, db.GENERATORS, generators_data)

    if project_settings[db.RESULTS][db.RUN]:
        logger.info(f'{info}genrating results')
        num_samples = project_settings[db.RESULTS]["NUM_SAMPLES"]
        num_samples_per_generator = project_settings[db.RESULTS]["NUM_SAMPLES_PER_GENERATOR"]
        generators_data = db.get_columns(search_conditions, db.GENERATORS)
        generators = generators_data[db.NETWORK]
        gen_weights = generators_data[db.WEIGHTS]

        regressor_data = db.get_columns(search_conditions, db.REGRESSOR)
        regressor = regressor_data[db.NETWORK]
        regressor.set_weights([np.array(x) for x in regressor_data[db.WEIGHTS]])
        
        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
        consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
        _, consumption = get_run_periods(consumption_df)
        m_consumption = consumption.mean(axis=1).values.T
        total_consumption = m_consumption.sum()
        
        results = dict()
        parameters = pd.DataFrame(columns = parameters_df.index)
 
        for i in range(num_samples):
            if i == len (generators):
                logger.info(f"{info}NUM_SAMPLES are more than generators.")
                break
            generators[i].set_weights([np.array(x) for x in gen_weights[i]])
            p_parameters = predict(generators[i], num_examples = num_samples_per_generator)
            m = i * num_samples_per_generator
            for p in range(num_samples_per_generator):
                parameters.loc[f'p_{m+p}'] = p_parameters[p]
        parameters.reset_index(inplace=True, drop=True)

        results[db.PARAMETERS] = parameters
        results[db.PREDICTIONS] = pd.DataFrame(predict(regressor, X=parameters[parameters_df.index]), columns=consumption_df["Name"])
        results[db.TOTAL] = pd.Series(results[db.PREDICTIONS].sum(axis=1))
        
        results[db.ERRORS] = pd.DataFrame(100 * (results[db.PREDICTIONS].values - m_consumption) / m_consumption, columns=consumption_df["Name"])
        results[db.TOTAL_ERROR] = pd.Series(100 * (results[db.TOTAL].values - total_consumption) / total_consumption,)
        
        db.update_columns(search_conditions, db.RESULTS, results)
