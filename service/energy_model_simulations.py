from Helper.geometry_helper import check_surfaces_cardinality
from . import os, pd, shutil, logger, tmp_dir, json
import copy
from service import db_functions as db

from runEP import execute_simulations

from Helper.Modules import *

from Helper.ConstructionHelper import create_construction_materials, InitialiseZoneSurfaces, get_construction_names, SetBestMatchInternalMass, get_material_names
from Helper.InfiltrationHelper import SetBestMatchPermeability

from Helper.ScheduleHelper import fill_schedules, set_setpoints
from Helper.RunPeriodHelper import get_run_periods
from Helper.HVACHelper.heatpump_with_boiler import add_heatpumps
from Helper.HVACHelper.baseboard_heating import add_baseboard_heating
from Helper.HVACHelper.SystemEfficiencyHelper import SetBestMatchSystemParameter
from Helper.ShadingHelper import AddShading

from Helper.InternalHeatGainsHelper import SetBestMatchInternalHeatGains

from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction
from Probabilistic.Parameter import ProbabilisticParameters

def generate_simulation_results(info: str,
                                idf_folder: str,
                                building_use: str,
                                simulation_settings: dict,
                                geometry_json: dict,
                                dummy_json: dict,
                                parameters_df: pd.DataFrame,
                                consumption_df: pd.DataFrame):
    
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
    return samples, energy_predictions

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
        messages = check_surfaces_cardinality(zone)
        for m in messages: logger.info(m)
        if any(messages): 
            print ('\n'.join((str(x) for x in messages)))

        ep_objects.append(zone.GenerateInternalMass(simulation_settings["SIMULATION_DEFAULTS"]["ZONE"]["INTERNAL_MASS"], mass_internal_mass))
        ep_objects.append(zone.get_infiltration_object(simulation_settings["SIMULATION_DEFAULTS"]["ZONE"]["INFILTRATION"]))

    zonelists = list(x for x in ep_objects if isinstance(x, Zonelist)) 
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