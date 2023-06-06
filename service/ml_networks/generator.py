from helper.run_period_helper import get_run_periods
from ml_models import get_generator, predict, get_regressor
from probabilistic.energy_predictions import ProbabilisticEnergyPrediction
from probabilistic.parameter import ProbabilisticParameters
from service.ml_networks import sample_hyperparameters
from service import logger, np, statuses, pd
from service import db_functions as db
import traceback

def run_generator(project_settings, info, search_conditions):
    db.update_columns(search_conditions, db.STATUS, statuses.TRAINING_GENERATOR)
    try:
        db.update_columns(search_conditions, db.GENERATORS, None)
        regressor = None
        if project_settings[db.GENERATOR_SETTINGS][db.METHOD] != db.INVERTED:
            regressor_data = db.get_columns(search_conditions, db.REGRESSOR)
            regressor = regressor_data[db.NETWORK]
            regressor.set_weights([np.array(x) for x in regressor_data[db.WEIGHTS]])
        
        consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
        _, consumption = get_run_periods(consumption_df)

        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
        p_parameters = ProbabilisticParameters.from_df(parameters_df)
        generators = train_generator(   info, search_conditions,
                                        p_parameters,
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
        project_settings[db.GENERATOR_SETTINGS][db.RUN] = False
        project_settings[db.RESULTS][db.RUN] = True
        db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        db.update_columns(search_conditions, db.STATUS, statuses.FAILED_GENERATOR)

def train_generator(info, search_conditions, p_parameters: ProbabilisticParameters, regressor, consumption, hyperparameters: dict, NUMS: int, **kwargs):
    hyperparameters = sample_hyperparameters(hyperparameters, NUMS,)
    logger.info(f'{info}training generator')
    if kwargs.get(db.METHOD) == db.GENERATIVE:
        targets = np.array([consumption.mean(axis=1) for _ in range(125)])
        generators = get_generator(hyperparameters, 
                                   p_parameters.get_scaling_df(), 
                                   regressor, targets, 
                                   error_domain=kwargs.get(db.ERROR_DOMAIN))
        for i, x in enumerate(generators):
            logger.info(f'{info}Generator Loss {i}:\t{x[1]:.5f}\t{hyperparameters.loc[i].values}')
            yield x
    elif kwargs.get(db.METHOD) == db.INVERTED:
        logger.info(f'{info}training inverted regressor')
        sampled_parameters = db.get_columns(search_conditions, db.SAMPLED_PARAMETERS, True)
        simulation_results = db.get_columns(search_conditions, db.SIMULATION_RESULTS,)
        regressor_targets = ProbabilisticEnergyPrediction.from_json(simulation_results).Values["Total"]
        scaling_df_Y=p_parameters.get_scaling_df()

        x = train_inverted_regressor(info, hyperparameters, regressor_targets, sampled_parameters, scaling_df_Y,)
        yield x

def train_inverted_regressor(info, 
                             hyperparameters: pd.DataFrame, 
                             inputs: np.ndarray, 
                             targets: np.ndarray, 
                             scaling_df_Y: pd.DataFrame, 
                             ):
    network, loss = get_regressor(hyperparameters, inputs, targets, scaling_df_Y=scaling_df_Y, inverted=True)
    logger.info(f'{info}Inverted Regressor Loss:\t{loss:.5f}')
    return network, loss

def predict_parameters(generator, regressor, num_samples_per_generator):
    parameters = predict(generator, None, num_samples_per_generator)
    results = predict(regressor, parameters,)
    return parameters, results