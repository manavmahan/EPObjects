from helper.run_period_helper import get_run_periods
from ml_models import predict, get_scaling_layer
from service import logger, np, pd, statuses
from service import db_functions as db
import traceback

def run_results(project_settings, info, search_conditions):
    db.update_columns(search_conditions, db.STATUS, statuses.GENERATING_RESULTS)
    try:
        db.update_columns(search_conditions, db.RESULTS, None)
        logger.info(f'{info}generating results')
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
        consumption = consumption.mean(axis=1)
        m_consumption = consumption.values.T
        total_consumption = m_consumption.sum()
        
        results = dict()
        parameters = pd.DataFrame(columns = parameters_df.index)

        if project_settings[db.GENERATOR_SETTINGS][db.METHOD] == db.INVERTED:
            X = consumption.values  
            X = X.reshape(1, -1)
        else:
            X = None
        for i in range(num_samples):
            if i == len (generators):
                logger.info(f"{info}NUM_SAMPLES are more than generators.")
                break

            generators[i].set_weights([np.array(x) for x in gen_weights[i]])

            p_parameters = predict(generators[i], X, num_examples = num_samples_per_generator)
            m = i * num_samples_per_generator
            for p in range(num_samples_per_generator):
                parameters.loc[f'p_{m+p}'] = p_parameters[p]
        parameters.reset_index(inplace=True, drop=True)

        predictions = predict(regressor, X=parameters[parameters_df.index])
        scaling_data = db.get_columns(search_conditions, db.SCALING)
        scaling_df_y = pd.DataFrame.from_dict(scaling_data[db.SCALING_DF_Y])
        predictions = get_scaling_layer(scaled_df=scaling_df_y, reverse=True)(predictions).numpy()

        results[db.PARAMETERS] = parameters
        results[db.PREDICTIONS] = pd.DataFrame(predictions, columns=consumption_df["Name"])
        results[db.TOTAL] = pd.Series(results[db.PREDICTIONS].sum(axis=1))
        
        results[db.ERRORS] = pd.DataFrame(100 * (results[db.PREDICTIONS].values - m_consumption) / m_consumption, columns=consumption_df["Name"])
        results[db.TOTAL_ERROR] = pd.Series(100 * (results[db.TOTAL].values - total_consumption) / total_consumption,)
        
        db.update_columns(search_conditions, db.RESULTS, results)
        db.update_columns(search_conditions, db.STATUS, statuses.UPDATED)
        project_settings[db.RESULTS][db.RUN] = False
        db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        db.update_columns(search_conditions, db.STATUS, statuses.FAILED_RESULTS)