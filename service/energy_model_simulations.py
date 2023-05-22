from . import os, pd, shutil, logger, tmp_dir, json
from service import db_functions as db

from runEP import ExecuteSimulations

from Helper.Modules import *

from Helper.ConstructionHelper import CreateConstructions, SetBestMatchConstruction, InitialiseZoneSurfaces, SetInternalMass, get_construction_names, SetBestMatchInternalMass, get_material_names
from Helper.InfiltrationHelper import SetBestMatchPermeability

from Helper.ScheduleHelper import get_schedules, SetBestMatchSetpoints
from Helper.RunPeriodHelper import get_run_periods
from Helper.HVACHelper.HeatPumpWithBoiler import AddHeatPumps
from Helper.HVACHelper.baseboard_heating import add_baseboard_heating
from Helper.HVACHelper.SystemEfficiencyHelper import SetBestMatchSystemParameter
from Helper.ShadingHelper import AddShading

from Helper.InternalHeatGainsHelper import SetBestMatchInternalHeatGains

from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction
from Probabilistic.Parameter import ProbabilisticParameters

def generate_simulation_results(info: str, idf_folder: str,
                                building_use: str,
                                simulation_settings: dict, 
                                geometry_json: dict, 
                                schedules_json: dict, 
                                parameters_df: pd.DataFrame,
                                consumption_df: pd.DataFrame):
    
    logger.info(f'{info}generating IDF files')
    samples = create_energyplus_models(idf_folder,
                                       building_use,
                                       simulation_settings,
                                       geometry_json, 
                                       schedules_json, 
                                       parameters_df,
                                       consumption_df)
    
    try:
        logger.info(f'{info}starting simulations')
        os.system(f'python3 runEP.py {idf_folder}')
        
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
                             schedules_json: dict,
                             parameters_df: pd.DataFrame,
                             consumption_df: pd.DataFrame):
    
    num_samples = simulation_settings["NUM_SAMPLES"]
    run_periods, _ = get_run_periods(consumption_df)

    ep_objects = list(db.get_auxiliary_objects())
    ep_objects += geometry_json
    
    construction_names = list(set(get_construction_names(ep_objects)))
    ep_objects += list(db.get_construction_material(construction_names))
    
    material_names = list(set(get_material_names(ep_objects)))
    ep_objects += list(db.get_construction_material(material_names, False))
    
    ep_objects += run_periods
    ep_objects += get_schedules(schedules_json["SCHEDULES"], schedules_json["SCHEDULE_TYPES"])
    
    InitialiseZoneSurfaces(ep_objects)
    SetInternalMass(ep_objects, simulation_settings["SIMULATION_DEFAULTS"]["ZONE"]["INTERNAL_MASS"])

    zones = list(x for x in ep_objects if isinstance(x, Zone))
    for zone in zones:
        ep_objects += [zone.GetInfiltrationObject(simulation_settings["SIMULATION_DEFAULTS"]["ZONE"]["INFILTRATION"])]

    zoneLists = list(x for x in ep_objects if isinstance(x, ZoneList)) 
    for zoneList in zoneLists:
        ep_objects += db.get_zonelist_settings(building_use, zoneList.Name)

    if simulation_settings["ENERGY_SYSTEM"] == "Heat Pumps":
        AddHeatPumps(ep_objects)

    if simulation_settings["ENERGY_SYSTEM"] == "Baseboard Heating":
        add_baseboard_heating(ep_objects)
    
    if simulation_settings["INTERNAL_SHADING"]:
        AddShading(ep_objects)

    pps = ProbabilisticParameters.from_df(parameters_df)
    samples = pps.GenerateSamplesAsDF(num_samples,)

    for i, sample in samples.iterrows():
        ep_objects_copy = list(ep_objects)
        CreateConstructions(sample, ep_objects_copy)
        SetBestMatchConstruction(ep_objects_copy)
        SetBestMatchInternalMass(sample, ep_objects_copy)
        SetBestMatchPermeability(sample, ep_objects_copy)
        SetBestMatchSetpoints(sample, ep_objects_copy, schedules_json["SCHEDULES"])
        SetBestMatchInternalHeatGains(sample, ep_objects_copy)
        SetBestMatchSystemParameter(sample, ep_objects_copy)

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