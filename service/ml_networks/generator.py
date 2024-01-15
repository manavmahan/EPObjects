"""Generator methods."""

import math
from helper.run_period import get_run_periods
from ml_models import get_generator, get_regressor, get_scaling_layer, get_scaling_parameters
from probabilistic.energy_predictions import ProbabilisticEnergyPrediction
from probabilistic.probabilistic_parameters import ProbabilisticParameters
from service.helper import logger, np, pd
from service import status
from service import db_functions as db
import traceback


def run_generator(project_settings, info, search_conditions):
    """Run generator."""
    db.update_columns(search_conditions, db.STATUS, status.TRAINING_GENERATOR)
    try:
        execute_generator(project_settings, info, search_conditions)
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        db.update_columns(
            search_conditions, db.STATUS, status.FAILED_GENERATOR)


def train_generator(
        info,
        search_conditions,
        p_parameters,
        hyperparameters,
        **kwargs):
    """Train generator."""
    regressor_data = db.get_columns(search_conditions, db.REGRESSOR)
    regressor = regressor_data[db.NETWORK]
    regressor.set_weights([np.array(x) for x in regressor_data[db.WEIGHTS]])
    
    scaling_data = db.get_columns(search_conditions, db.SCALING)
    scaling_df_y = pd.DataFrame.from_dict(scaling_data[db.SCALING_DF_Y])
    
    consumption_df = db.get_columns(search_conditions, db.CONSUMPTION, True)
    _, consumption = get_run_periods(consumption_df)
    
    targets = np.array([consumption.mean(axis=1) for _ in range(50)])
    targets = get_scaling_layer(scaled_df=scaling_df_y)(targets).numpy()
    x = get_generator(hyperparameters.loc[0],
        p_parameters.get_scaling_df(),
        regressor, targets,
        error_domain=kwargs.get(db.ERROR_DOMAIN))

    logger.info(f'{info}Generator Loss:\t{x[1]:.5f}')
    return x


def train_inverted_regressor(
        info, search_conditions,
        hyperparameters: pd.DataFrame,
        p_parameters,):
    """Train regressor."""
    logger.info(f'{info}training inverted regressor')
    sampled_parameters = db.get_columns(
        search_conditions, db.SAMPLED_PARAMETERS, True)
    simulation_results = db.get_columns(
        search_conditions, db.SIMULATION_RESULTS,)
    regressor_targets = ProbabilisticEnergyPrediction.from_json(
        simulation_results).Values["Total"]
    
    scaling_df_X = get_scaling_parameters(regressor_targets, all_columns_equal=True)
    scaling_df_Y = p_parameters.get_scaling_df()

    network, loss = get_regressor(
        hyperparameters, regressor_targets, sampled_parameters, scaling_df_X=scaling_df_X,
        scaling_df_Y=scaling_df_Y, inverted=True)
    logger.info(f'{info}Inverted Regressor Loss:\t{loss:.5f}')
    return (network, loss)

def execute_generator(project_settings, info, search_conditions):
    """Execute generator."""
    db.update_columns(search_conditions, db.GENERATORS, None)

    parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
    p_parameters = ProbabilisticParameters.from_df(parameters_df)

    gen_type = project_settings[db.GENERATOR_SETTINGS][db.METHOD].lower()
    hp = db.get_hyperparameters_all(network=gen_type)

    if project_settings[db.GENERATOR_SETTINGS][db.METHOD] == db.GENERATIVE:
        network, loss = train_generator(info, search_conditions,
            p_parameters, hp, **project_settings[db.GENERATOR_SETTINGS])
    else:
        network, loss = train_inverted_regressor(
            info, search_conditions, hp.loc[0], p_parameters)

    generators_data = {db.NETWORK: network, db.LOSS: loss, db.WEIGHTS: network.get_weights()}
    
    db.update_columns(search_conditions, db.GENERATORS, generators_data)
    project_settings[db.GENERATOR_SETTINGS][db.RUN] = False
    project_settings[db.RESULTS][db.RUN] = True
    db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)
