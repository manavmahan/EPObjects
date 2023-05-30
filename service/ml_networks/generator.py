from helper.run_period_helper import get_run_periods
from ml_models import get_generator, predict, get_scaling_parameters
from probabilistic.parameter import ProbabilisticParameters
from service.ml_networks import sample_hyperparameters
from service import logger, np, statuses
from service import db_functions as db

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
        project_settings[db.GENERATOR_SETTINGS][db.RUN] = False
        project_settings[db.RESULTS][db.RUN] = True
        db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)
    except Exception as e:
        logger.info(e)
        db.update_columns(search_conditions, db.STATUS, statuses.FAILED_GENERATOR)

def train_generator(info, probabilistic_parameters, regressor, consumption, hyperparameters: dict, NUMS: int, **kwargs):
    hyperparameters = sample_hyperparameters(hyperparameters, NUMS,)
    logger.info(f'{info}training generator')
    if kwargs.get(db.METHOD) == db.GENERATIVE:
        targets = np.array([consumption.mean(axis=1) for _ in range(125)])
        for i, x in enumerate(get_generator(hyperparameters, probabilistic_parameters.GetScalingDF(), regressor, targets, )):
            logger.info(f'{info}Generator Loss {i}:\t{x[1]:.5f}')
            yield x

def predict_parameters(generator, regressor, num_samples_per_generator):
    parameters = predict(generator, None, num_samples_per_generator)
    results = predict(regressor, parameters,)
    return parameters, results