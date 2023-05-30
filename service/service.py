from service import np, pd, create_simulation_dir, logger
import service.db_functions as db

from probabilistic.energy_predictions import ProbabilisticEnergyPrediction
from probabilistic.parameter import ProbabilisticParameters

from service.energy_model_simulations import generate_simulation_results, get_run_periods
from service.ml_networks import train_generator, train_regressor, predict, get_scaling_parameters

def run_service(user_name, project_name):
    info = f'User: {user_name}\tProject: {project_name}\t'
    search_conditions = db.get_search_conditions(user_name, project_name)

    project_settings = db.get_columns(search_conditions, db.PROJECT_SETTINGS,)

    if project_settings[db.SIMULATION_SETTINGS][db.RUN]:
        building_use = project_settings[db.BUILDING_USE]
        idf_folder = create_simulation_dir(user_name, project_name, project_settings[db.LOCATION])
        geometry_json = db.get_columns(search_conditions, db.GEOMETRY,)
        dummy_objects_json = db.get_columns(search_conditions, db.DUMMY_OBJECTS)
        consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)

        results = generate_simulation_results(
            info, idf_folder, building_use,
            project_settings[db.SIMULATION_SETTINGS], 
            geometry_json, dummy_objects_json,
            parameters_df, consumption_df,
        )
        for column in results:
            db.update_columns(search_conditions, column, results[column])

    if project_settings[db.REGRESSOR_SETTINGS][db.RUN]:
        sampled_parameters = db.get_columns(search_conditions, db.SAMPLED_PARAMETERS, True)
        simulation_results = db.get_columns(search_conditions, db.SIMULATION_RESULTS,)
        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
        parameters = ProbabilisticParameters.from_df(parameters_df)

        regressor_targets = ProbabilisticEnergyPrediction.from_json(simulation_results).Values["Total"]
        network, loss = train_regressor(info, parameters, sampled_parameters, regressor_targets, db.get_regressor_hyperparameters(search_conditions), **project_settings[db.REGRESSOR_SETTINGS])
        db.update_columns(search_conditions, db.REGRESSOR, {db.NETWORK: network, db.LOSS: loss, db.WEIGHTS: network.get_weights()},)
        db.update_columns(search_conditions, db.SCALING, {db.PARAMETERS: parameters.GetScalingDF(), db.PREDICTIONS: get_scaling_parameters(regressor_targets, all_columns_equal=True)},)

    if project_settings[db.GENERATOR_SETTINGS][db.RUN]:
        regressor = None
        if project_settings[db.GENERATOR_SETTINGS][db.METHOD] != db.INVERTED:
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
                                        consumption, 
                                        db.get_genertor_hyperparameters(search_conditions),
                                        **project_settings[db.GENERATOR_SETTINGS])

        generators_data = None #db.get_columns(search_conditions, db.GENERATORS)
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
