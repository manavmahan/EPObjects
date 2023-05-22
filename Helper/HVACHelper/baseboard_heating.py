from Helper.Modules import *
from IDFObject.HVACTemplate.Plant.HotWaterLoop import HotWaterLoop
from IDFObject.HVACTemplate.Zone.BaseboardHeat import BaseboardHeat
from IDFObject.Output.Variable import Variable

def add_baseboard_heating(ep_objects, boiler_fuel_type="NaturalGas"):
    zones = list (x for x in ep_objects if isinstance(x, Zone))
    zonelists = list (x for x in ep_objects if isinstance(x, ZoneList))
    for zone in zones:
        zonelist_name = next(x for x in zonelists if zone.Name in x.IDF).Name
        zone_bh = get_zone_baseboard_heating(zone, zonelist_name)
        ep_objects.append(zone_bh)

    ep_objects.append(Variable(
        Name = "Zone Air System Sensible Heating Rate"))

    ep_objects.append(HotWaterLoop())
    ep_objects.append(
        Boiler(
            FuelType = boiler_fuel_type
        )
    )
    boiler_fuel_output = "Electricity"
    if boiler_fuel_type in ["NaturalGas"]:
        boiler_fuel_output = 'Gas'
    output_variable_name = f"Boiler {boiler_fuel_type} Energy"
    ep_objects.append(Variable(
        Name = output_variable_name))

def get_zone_baseboard_heating(zone, zonelist_name):
    return BaseboardHeat(
        ZoneName = zone.Name,
        TemplateThermostatName = f'Thermostat.{zonelist_name}'
    )