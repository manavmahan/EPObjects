"""Simulation methods."""
import copy
import math
import os
import pandas as pd
import traceback

from logger import logger
from run_ep import execute_simulations

from helper.geometry import check_surfaces_cardinality
from helper.construction import InitialiseZoneSurfaces
from idf_object.zone import Zone

from service.helper import create_simulation_dir
import service.db_functions as db
import service.status as status
from .read_simulations import read_simulations
from .create_energyplus_models import create_energyplus_models


def run_simulations(user_name, project_name,
                    project_settings, info, search_conditions):
    """Run simulations on a project."""
    db.update_columns(search_conditions, db.STATUS, status.RUNNING_SIMULATIONS)

    try:
        db.update_columns(search_conditions, db.SAMPLED_PARAMETERS, None)
        db.update_columns(search_conditions, db.SIMULATION_RESULTS, None)

        building_use = project_settings[db.BUILDING_USE]
        idf_folder = create_simulation_dir(
            user_name, project_name, project_settings[db.LOCATION])
        geometry_json = db.get_columns(
            search_conditions, db.GEOMETRY,)
        dummy_objects_json = db.get_columns(
            search_conditions, db.DUMMY_OBJECTS)
        constructions_json = db.get_columns(
            search_conditions, db.CONSTRUCTIONS)
        consumption_df = db.get_columns(
            search_conditions, db.CONSUMPTION, True)
        parameters_df = db.get_columns(
            search_conditions, db.PARAMETERS, True)

        results = generate_simulation_results(
            info, idf_folder, building_use,
            project_settings[db.SIMULATION_SETTINGS],
            geometry_json, dummy_objects_json,
            constructions_json,
            parameters_df, consumption_df,
        )
        for column in results:
            db.update_columns(search_conditions, column, results[column])
        project_settings[db.SIMULATION_SETTINGS][db.RUN] = False
        project_settings[db.REGRESSOR_SETTINGS][db.RUN] = True
        project_settings[db.GENERATOR_SETTINGS][db.RUN] = True
        project_settings[db.RESULTS][db.RUN] = True
        db.update_columns(
            search_conditions, db.PROJECT_SETTINGS, project_settings)
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        db.update_columns(
            search_conditions, db.STATUS, status.FAILED_SIMULATIONS)


def generate_simulation_results(info: str,
                                idf_folder: str,
                                building_use: str,
                                simulation_settings: dict,
                                geometry_json: dict,
                                dummy_json: dict,
                                constructions_json: dict,
                                parameters_df: pd.DataFrame,
                                consumption_df: pd.DataFrame):
    """Run simulations and read results."""
    clean_up_geometry(geometry_json)
    logger.info(f'{info}generating IDF files')
    samples = create_energyplus_models(idf_folder,
                                       building_use,
                                       simulation_settings,
                                       geometry_json,
                                       dummy_json,
                                       constructions_json,
                                       parameters_df,
                                       consumption_df)
    try:
        logger.info(f'{info}starting simulations')
        execute_simulations(idf_folder)
        logger.info(f'{info}reading simulation results')
        energy_predictions = read_simulations(
            simulation_settings["NUM_SAMPLES"],
            list(consumption_df['Name']),
            idf_folder)
    except FileNotFoundError:
        error_file = os.path.join(idf_folder, "0.err")
        if not os.path.isfile(error_file):
            error_file = os.path.join(idf_folder,
                                      "Temp", "EP_0", "eplusout.err")
        idf_file = os.path.join(idf_folder, "0.idf",)
        if error_file:
            with open(error_file) as f:
                info = f.readlines()
        with open(idf_file) as f:
            info += f.readlines()
        raise FileNotFoundError("".join(info))
    return {db.SAMPLED_PARAMETERS: samples,
            db.SIMULATION_RESULTS: energy_predictions, }


def clean_up_geometry(geometry_json: list(),):
    """Clean up geometry for EnergyPlus models."""
    InitialiseZoneSurfaces(geometry_json)
    zones = list(x for x in geometry_json if isinstance(x, Zone))
    for zone in zones:
        messages = check_surfaces_cardinality(zone)
        for m in messages:
            logger.info(m)
