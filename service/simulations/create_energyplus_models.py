"""Create energyplus models."""
import copy
import math
import pandas as pd

from helper.construction import create_construction_materials
from helper.construction import InitialiseZoneSurfaces
from helper.construction import get_generic_construction_names
from helper.construction import SetBestMatchInternalMass
from helper.construction import get_material_names
from helper.infiltration import SetBestMatchPermeability

from helper.schedule import fill_schedules, set_setpoints
from helper.run_period import get_run_periods
from helper.hvac.heatpump_with_boiler import add_heatpumps
from helper.hvac.baseboard_heating import add_baseboard_heating
from helper.hvac.system_efficiency_helper import SetBestMatchSystemParameter
from helper.shading import AddShading
from helper.internal_heat_gains import SetBestMatchInternalHeatGains
from helper.hot_water import set_hot_water_rate

from probabilistic.probabilistic_parameters import ProbabilisticParameters

from idf_object.scheduletypelimits import ScheduleTypeLimits
from idf_object.zone import Zone
from idf_object.zonelist import ZoneList

import service.db_functions as db


def create_energyplus_models(idf_folder: str,
                             building_use: str,
                             sim_settings: dict,
                             geometry_json: dict,
                             dummy_json: dict,
                             constructions_json: dict,
                             parameters_df: pd.DataFrame,
                             consumption_df: pd.DataFrame):
    """Create EnergyPlus models using project data."""
    num_samples = sim_settings["NUM_SAMPLES"]
    run_periods, _ = get_run_periods(consumption_df)

    ep_objects = list(db.get_auxiliary_objects())
    ep_objects += run_periods
    ep_objects += geometry_json
    ep_objects += dummy_json
    constructions = constructions_json
    InitialiseZoneSurfaces(ep_objects)

    construction_names = get_generic_construction_names(
        ep_objects, constructions)
    constructions += list(db.get_construction_material(
        construction_names))

    material_names = get_material_names(constructions)
    generic_materials = list(db.get_construction_material(
        list(set(material_names["Name"])), False))
    materials = []
    for m in material_names.index:
        material = copy.deepcopy(
            next(x for x in generic_materials
                 if x.Name == material_names.loc[m, 'Name']))
        material.Name = m
        if (not math.isnan(material_names.loc[m, 'Thickness']) and
                hasattr(material, 'Thickness')):
            material.Thickness = material_names.loc[m, 'Thickness'] / 1000
        materials.append(material)

    for c in constructions:
        c.initialise_materials(materials)

    zones = list(x for x in ep_objects if isinstance(x, Zone))
    mass_material = next(x for x in materials if x.Name == "Mass")
    mass_internal_mass = mass_material.Thickness *\
        mass_material.Density *\
        mass_material.SpecificHeat / 1000

    im_per_sq_m = sim_settings["SIMULATION_DEFAULTS"]["ZONE"]["INTERNAL_MASS"]
    infiltration = sim_settings["SIMULATION_DEFAULTS"]["ZONE"]["INFILTRATION"]
    for zone in zones:
        ep_objects.append(zone.GenerateInternalMass(
            im_per_sq_m, mass_internal_mass))
        ep_objects.append(zone.get_infiltration_object(infiltration))

    zonelists = list(x for x in ep_objects if isinstance(x, ZoneList))
    for zonelist in zonelists:
        ep_objects += db.get_zonelist_settings(building_use, zonelist.Name)
    ep_objects.append(ScheduleTypeLimits())

    if sim_settings["ENERGY_SYSTEM"] == "Heat Pumps":
        add_heatpumps(ep_objects)

    if sim_settings["ENERGY_SYSTEM"] == "Baseboard Heating":
        add_baseboard_heating(ep_objects)

    if sim_settings["INTERNAL_SHADING"]:
        AddShading(ep_objects)

    pps = ProbabilisticParameters.from_df(parameters_df)
    samples = pps.generate_samples_as_df(num_samples,)

    for i, sample in samples.iterrows():
        ep_objects_copy = copy.deepcopy(ep_objects)
        ep_objects_copy += create_construction_materials(
            sample, constructions, materials)

        SetBestMatchInternalMass(sample, ep_objects_copy)
        SetBestMatchPermeability(sample, ep_objects_copy)
        SetBestMatchInternalHeatGains(sample, ep_objects_copy)
        SetBestMatchSystemParameter(sample, ep_objects_copy)
        set_setpoints(sample, ep_objects_copy)
        fill_schedules(sample, ep_objects_copy)
        set_hot_water_rate(sample, ep_objects_copy)

        with open(f'{idf_folder}/{i}.idf', 'w') as f:
            f.write('\n'.join((x.IDF for x in ep_objects_copy)))
    return samples
