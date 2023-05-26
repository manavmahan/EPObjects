from Helper.Modules import *
from IDFObject.HVACTemplate.Plant.HotWaterLoop import HotWaterLoop
from IDFObject.HVACTemplate.Zone.BaseboardHeat import BaseboardHeat
from IDFObject.HVACTemplate.Thermostat import Thermostat
from IDFObject.Output.Variable import Variable
from IDFObject.Schedule.Compact import Compact

from Helper.HVACHelper import get_zonelists_with_thermostat

def add_baseboard_heating(ep_objects, boiler_fuel_type="NaturalGas"):
    thermostats = list (x for x in ep_objects if isinstance(x, Thermostat))
    zonelists = list (x for x in ep_objects if isinstance(x, Zonelist))

    for zonelist in get_zonelists_with_thermostat(zonelists, thermostats):
        for zone in zonelist.ZoneNames:
            zone_bh = get_zone_baseboard_heating(zone, zonelist.Name)
            ep_objects.append(zone_bh)

    ep_objects.append(Variable(
        Name = "Zone Air System Sensible Heating Rate"))

    ep_objects.append(HotWaterLoop())
    ep_objects.append(
        Boiler(
            FuelType = boiler_fuel_type
        )
    )
    output_variable_name = f"Boiler {boiler_fuel_type} Energy"
    ep_objects.append(Variable(
        Name = output_variable_name))

def get_zone_baseboard_heating(zone_name, zonelist_name,):
    thermostat_name = f'Thermostat.{zonelist_name}'
    return BaseboardHeat(
        ZoneName = zone_name,
        TemplateThermostatName = thermostat_name
    )