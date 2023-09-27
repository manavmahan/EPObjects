"""Regressor methods."""
import numpy as np
from probabilistic.energy_predictions import ProbabilisticEnergyPrediction
from probabilistic.probabilistic_parameters import ProbabilisticParameters
from service import status
import traceback

from logger import logger
from ml_models import get_regressor, get_scaling_parameters
from service import db_functions as db

from .helper import sample_hyperparameters


def run_regressor(project_settings, info, search_conditions):
    """Run regresson on project data."""
    db.update_columns(search_conditions, db.STATUS, status.TRAINING_REGRESSOR)
    try:
        execute_regressor(project_settings, info, search_conditions)
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        db.update_columns(
            search_conditions, db.STATUS, status.FAILED_REGRESSOR)


def execute_regressor(project_settings, info, search_conditions):
    """Execute train regressor."""
    db.update_columns(search_conditions, db.REGRESSOR, None)
    db.update_columns(search_conditions, db.SCALING, None)

    sampled_parameters = db.get_columns(
        search_conditions, db.SAMPLED_PARAMETERS, True)
    simulation_results = db.get_columns(
        search_conditions, db.SIMULATION_RESULTS,)
    parameters_df = db.get_columns(
        search_conditions, db.PARAMETERS, True)
    p_parameters = ProbabilisticParameters.from_df(parameters_df)

    regressor_targets = ProbabilisticEnergyPrediction.from_json(
        simulation_results).Values["Total"]
    network, scaling_df_y, loss = train_regressor(
        info, p_parameters, sampled_parameters, regressor_targets,
        db.get_regressor_hyperparameters(search_conditions),
        nums=project_settings[db.REGRESSOR_SETTINGS][db.NUMS])

    db.update_columns(search_conditions, db.REGRESSOR,
                      {db.NETWORK: network,
                       db.LOSS: loss,
                       db.WEIGHTS: network.get_weights()},)

    scale_y = get_scaling_parameters(regressor_targets, all_columns_equal=True)
    db.update_columns(search_conditions, db.SCALING,
                      {db.PARAMETERS: p_parameters.get_scaling_df(),
                       db.PREDICTIONS: scale_y,
                       db.SCALING_DF_Y: scaling_df_y},)
    project_settings[db.REGRESSOR_SETTINGS][db.RUN] = False
    project_settings[db.GENERATOR_SETTINGS][db.RUN] = True
    project_settings[db.RESULTS][db.RUN] = True
    db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)


def train_regressor(
        info,
        probabilistic_parameters: ProbabilisticParameters,
        sampled_parameters: np.ndarray,
        target_values: np.ndarray,
        hyperparameters: dict,
        nums: int,
        **kwargs):
    """Train regressor."""
    logger.info(f'{info}Training Regressor')
    hyperparameters = sample_hyperparameters(hyperparameters, nums,)
    network, scaling_df_y, loss, epoch = get_regressor(
        hyperparameters, sampled_parameters, target_values,
        probabilistic_parameters.get_scaling_df(),)
    logger.info(f'{info}Regressor Loss:\t{loss:.5f}\tEpochs:{epoch}')
    return network, scaling_df_y, loss
