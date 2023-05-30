from probabilistic.energy_predictions import ProbabilisticEnergyPrediction
from probabilistic.parameter import ProbabilisticParameters
from service import logger, os, np, pd, shutil, statuses, tmp_dir

from service import db_functions as db
from ml_models import get_regressor, get_generator, predict, get_scaling_parameters
from service.ml_networks import sample_hyperparameters

def run_regressor(project_settings, info, search_conditions):
    db.update_columns(search_conditions, db.STATUS, statuses.TRAINING_REGRESSOR)
    try:
        db.update_columns(search_conditions, db.REGRESSOR, None)    
        db.update_columns(search_conditions, db.SCALING, None)

        sampled_parameters = db.get_columns(search_conditions, db.SAMPLED_PARAMETERS, True)
        simulation_results = db.get_columns(search_conditions, db.SIMULATION_RESULTS,)
        parameters_df = db.get_columns(search_conditions, db.PARAMETERS, True)
        parameters = ProbabilisticParameters.from_df(parameters_df)

        regressor_targets = ProbabilisticEnergyPrediction.from_json(simulation_results).Values["Total"]
        network, loss = train_regressor(info, parameters, sampled_parameters, regressor_targets, db.get_regressor_hyperparameters(search_conditions), **project_settings[db.REGRESSOR_SETTINGS])
        db.update_columns(search_conditions, db.REGRESSOR, {db.NETWORK: network, db.LOSS: loss, db.WEIGHTS: network.get_weights()},)
        db.update_columns(search_conditions, db.SCALING, {db.PARAMETERS: parameters.GetScalingDF(), db.PREDICTIONS: get_scaling_parameters(regressor_targets, all_columns_equal=True)},)
        project_settings[db.REGRESSOR_SETTINGS][db.RUN] = False
        project_settings[db.GENERATOR_SETTINGS][db.RUN] = True
        project_settings[db.RESULTS][db.RUN] = True
        db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)
    except Exception as e:
        logger.info(e)
        db.update_columns(search_conditions, db.STATUS, statuses.FAILED_REGRESSOR)

def train_regressor(info, probabilistic_parameters, sampled_parameters: np.ndarray, target_values: np.ndarray, hyperparameters: dict, NUMS: int, **kwargs):
    logger.info(f'{info}Training Regressor')
    hyperparameters = sample_hyperparameters(hyperparameters, NUMS,)
    network, loss = get_regressor(hyperparameters, sampled_parameters, target_values, probabilistic_parameters.GetScalingDF(),)
    logger.info(f'{info}Regressor Loss:\t{loss:.5f}')
    return network, loss