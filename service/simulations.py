from helper.geometry_helper import check_surfaces_cardinality
from . import os, pd, logger
import copy
import traceback
from service import db_functions as db
from service import statuses, create_simulation_dir

from run_ep import execute_simulations

from helper.construction_helper import create_construction_materials, InitialiseZoneSurfaces, get_construction_names, SetBestMatchInternalMass, get_material_names
from helper.infiltration_helper import SetBestMatchPermeability

from helper.schedule_helper import fill_schedules, set_setpoints
from helper.run_period_helper import get_run_periods
from helper.hvac_helper.heatpump_with_boiler import add_heatpumps
from helper.hvac_helper.baseboard_heating import add_baseboard_heating
from helper.hvac_helper.system_efficiency_helper import SetBestMatchSystemParameter
from helper.shading_helper import AddShading

from helper.internal_heat_gains_helper import SetBestMatchInternalHeatGains

from probabilistic.energy_predictions import EnergyPrediction, ProbabilisticEnergyPrediction
from probabilistic.parameter import ProbabilisticParameters

from idf_object.scheduletypelimits import ScheduleTypeLimits
from idf_object.zone import Zone
from idf_object.zonelist import ZoneList

def run_simulations(user_name, project_name, project_settings, info, search_conditions):
    db.update_columns(search_conditions, db.STATUS, statuses.RUNNING_SIMULATIONS)

    try:
        db.update_columns(search_conditions, db.SAMPLED_PARAMETERS, None)
        db.update_columns(search_conditions, db.SIMULATION_RESULTS, None)

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
        project_settings[db.SIMULATION_SETTINGS][db.RUN] = False
        project_settings[db.REGRESSOR_SETTINGS][db.RUN] = True
        project_settings[db.GENERATOR_SETTINGS][db.RUN] = True
        project_settings[db.RESULTS][db.RUN] = True
        db.update_columns(search_conditions, db.PROJECT_SETTINGS, project_settings)
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        db.update_columns(search_conditions, db.STATUS, statuses.FAILED_SIMULATIONS)

def generate_simulation_results(info: str,
                                idf_folder: str,
                                building_use: str,
                                simulation_settings: dict,
                                geometry_json: dict,
                                dummy_json: dict,
                                parameters_df: pd.DataFrame,
                                consumption_df: pd.DataFrame):
    clean_up_geometry(geometry_json)
    logger.info(f'{info}generating IDF files')
    samples = create_energyplus_models(idf_folder,
                                       building_use,
                                       simulation_settings,
                                       geometry_json,
                                       dummy_json,
                                       parameters_df,
                                       consumption_df)
    
    try:
        logger.info(f'{info}starting simulations')
        execute_simulations(idf_folder)
        logger.info(f'{info}reading simulation results')
        energy_predictions = read_simulations(simulation_settings["NUM_SAMPLES"], list(consumption_df['Name']), idf_folder)
    except FileNotFoundError:
        error_file = os.path.join(idf_folder, "0.err")
        if not os.path.isfile(error_file):
            error_file = os.path.join(idf_folder, "Temp", "EP_0", "eplusout.err")
        idf_file = os.path.join(idf_folder, "0.idf",)
        if error_file: 
            with open(error_file) as f: info = f.readlines()
        with open(idf_file) as f: info += f.readlines()
        raise FileNotFoundError("".join(info))
    return {db.SAMPLED_PARAMETERS: samples, db.SIMULATION_RESULTS: energy_predictions,}

def clean_up_geometry(geometry_json: list(),):
    InitialiseZoneSurfaces(geometry_json)
    zones = list(x for x in geometry_json if isinstance(x, Zone))
    for zone in zones:
        messages = check_surfaces_cardinality(zone)
        for m in messages: logger.info(m)

def create_energyplus_models(idf_folder: str,
                             building_use: str,
                             simulation_settings: dict,
                             geometry_json: dict,
                             dummy_json: dict,
                             parameters_df: pd.DataFrame,
                             consumption_df: pd.DataFrame):
    
    num_samples = simulation_settings["NUM_SAMPLES"]
    run_periods, _ = get_run_periods(consumption_df)

    ep_objects = list(db.get_auxiliary_objects())
    ep_objects += run_periods
    ep_objects += geometry_json
    ep_objects += dummy_json
    InitialiseZoneSurfaces(ep_objects)
    
    construction_names = get_construction_names(ep_objects)
    construction_names.append('Mass')
    constructions = list(db.get_construction_material(construction_names))
    
    material_names = get_material_names(constructions)
    materials = list(db.get_construction_material(list(material_names.keys()), False))
    for m in materials:
        if material_names[m.Name] is not None: m.Thickness = material_names[m.Name] / 1000

    for c in constructions:
        c.initialise_materials(materials)

    zones = list(x for x in ep_objects if isinstance(x, Zone))
    mass_material = next(x for x in materials if x.Name=="Mass")
    mass_internal_mass = mass_material.Thickness * mass_material.Density * mass_material.SpecificHeat / 1000
    
    for zone in zones:
        ep_objects.append(zone.GenerateInternalMass(simulation_settings["SIMULATION_DEFAULTS"]["ZONE"]["INTERNAL_MASS"], mass_internal_mass))
        ep_objects.append(zone.get_infiltration_object(simulation_settings["SIMULATION_DEFAULTS"]["ZONE"]["INFILTRATION"]))

    zonelists = list(x for x in ep_objects if isinstance(x, ZoneList)) 
    for zonelist in zonelists:
        ep_objects += db.get_zonelist_settings(building_use, zonelist.Name)
    ep_objects.append(ScheduleTypeLimits())

    if simulation_settings["ENERGY_SYSTEM"] == "Heat Pumps":
        add_heatpumps(ep_objects)

    if simulation_settings["ENERGY_SYSTEM"] == "Baseboard Heating":
        add_baseboard_heating(ep_objects)
    
    if simulation_settings["INTERNAL_SHADING"]:
        AddShading(ep_objects)

    pps = ProbabilisticParameters.from_df(parameters_df)
    samples = pps.GenerateSamplesAsDF(num_samples,)

    for i, sample in samples.iterrows():
        ep_objects_copy = copy.deepcopy(ep_objects)
        ep_objects_copy += create_construction_materials(sample, constructions, materials)

        SetBestMatchInternalMass(sample, ep_objects_copy)
        SetBestMatchPermeability(sample, ep_objects_copy)
        SetBestMatchInternalHeatGains(sample, ep_objects_copy)
        SetBestMatchSystemParameter(sample, ep_objects_copy)
        set_setpoints(sample, ep_objects_copy)
        fill_schedules(ep_objects_copy)

        with open(f'{idf_folder}/{i}.idf', 'w') as f:
            f.write('\n'.join((x.IDF for x in ep_objects_copy)))
    return samples

def read_simulations(num_samples: int, run_period_names: list, idf_folder: str):
    pEnergies = []
    for i in range(num_samples):
        data = pd.read_csv(f'{idf_folder}/{i}.csv', index_col=0)
        data = data[[c for c in data.columns if 'Energy' in c]]
        data.index = run_period_names
        pEnergies += [EnergyPrediction(None, data)]

    return ProbabilisticEnergyPrediction(None, pEnergies).to_dict()