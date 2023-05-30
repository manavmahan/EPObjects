from helper.run_period_helper import get_run_periods
from ml_models import predict
from service.ml_networks import sample_hyperparameters
from service import logger, np, pd, statuses
from service import db_functions as db

def run_results(project_settings, info, search_conditions):
    db.update_columns(search_conditions, db.STATUS, statuses.GENERATING_RESULTS)
    try:
        db.update_columns(search_conditions, db.RESULTS, None)
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
        db.update_columns(search_conditions, db.STATUS, statuses.UPDATED)
    except Exception as e:
        logger.info(e)
        db.update_columns(search_conditions, db.STATUS, statuses.FAILED_RESULTS)