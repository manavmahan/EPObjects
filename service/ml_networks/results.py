"""Generate results."""
import numpy as np
import pandas as pd

import traceback

from helper.run_period import get_run_periods
from ml_models import predict, get_scaling_layer
from logger import logger

from service import status
from service import db_functions as db


def run_results(project_settings, info, search_conditions):
    """Run results on a project."""
    db.update_columns(search_conditions, db.STATUS, status.GENERATING_RESULTS)
    try:
        execute_results(project_settings, info, search_conditions)
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        db.update_columns(search_conditions, db.STATUS, status.FAILED_RESULTS)


def execute_results(project_settings, info, search_conditions):
    """Execute results."""
    db.update_columns(search_conditions, db.RESULTS, None)
    logger.info(f'{info}generating results')
    num_samples = project_settings[db.RESULTS]["NUM_SAMPLES"]
    ns_per_gen = project_settings[db.RESULTS]["NUM_SAMPLES_PER_GENERATOR"]
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
    parameters = pd.DataFrame(columns=parameters_df.index)

    if project_settings[db.GENERATOR_SETTINGS][db.METHOD] == db.INVERTED:
        x = consumption.values
        x = x.reshape(1, -1)
    else:
        x = None
    for i in range(num_samples):
        if i == len(generators):
            logger.info(f"{info}NUM_SAMPLES are more than generators.")
            break

        generators[i].set_weights([np.array(x) for x in gen_weights[i]])

        p_parameters = predict(
            generators[i], x, num_examples=ns_per_gen)
        m = i * ns_per_gen
        for p in range(ns_per_gen):
            parameters.loc[f'p_{m+p}'] = p_parameters[p]
    parameters.reset_index(inplace=True, drop=True)

    predictions = predict(regressor, X=parameters[parameters_df.index])
    scaling_data = db.get_columns(search_conditions, db.SCALING)
    scaling_df_y = pd.DataFrame.from_dict(scaling_data[db.SCALING_DF_Y])
    predictions = get_scaling_layer(
        scaled_df=scaling_df_y, reverse=True)(predictions).numpy()

    results[db.PARAMETERS] = parameters
    results[db.PREDICTIONS] = pd.DataFrame(
        predictions, columns=consumption_df["Name"])
    results[db.TOTAL] = pd.Series(results[db.PREDICTIONS].sum(axis=1))

    errors = (results[db.PREDICTIONS].values - m_consumption)
    errors /= m_consumption
    results[db.ERRORS] = pd.DataFrame(
        100 * errors, columns=consumption_df["Name"])

    total_error = (results[db.TOTAL].values - total_consumption)
    total_error /= total_consumption

    # print(abs(results[db.ERRORS]).sum(axis=1))
    results[db.TOTAL_ERROR] = abs(results[db.ERRORS]).mean(axis=1)

    db.update_columns(search_conditions, db.RESULTS, results)
    db.update_columns(search_conditions, db.STATUS, status.UPDATED)
    project_settings[db.RESULTS][db.RUN] = False
    db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)
