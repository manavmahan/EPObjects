from Helper.Modules import *
from Helper.HVACHelper import get_zonelists_with_thermostat
from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump
from IDFObject.HVACTemplate.Thermostat import Thermostat
from IDFObject.Output.Variable import Variable

def add_heatpumps(ep_objects):
    thermostats = list (x for x in ep_objects if isinstance(x, Thermostat))
    zonelists = list (x for x in ep_objects if isinstance(x, Zonelist))

    for zonelist in get_zonelists_with_thermostat(zonelists, thermostats):
        for zone_name in zonelist.ZoneNames:
            zoneWAHP = GetWaterToAirHeatPumpObject(zone_name, zonelist.Name)
            ep_objects.append(zoneWAHP)

    ep_objects.append(MixedWaterLoop())
    ep_objects.append(Tower())
    ep_objects.append(Variable(
        Name = "Zone Air System Sensible Heating Rate"))
    ep_objects.append(Variable(
        Name = "Zone Air System Sensible Cooling Rate"))
    ep_objects.append(Variable(
        Name = "Zone Water to Air Heat Pump Electricity Energy"))
    ep_objects.append(Variable(
        Name = "Cooling Tower Fan Electricity Energy"))

def add_heatpumps_with_boiler(epObjects):
    add_heatpumps(epObjects)
    boiler = Boiler(Boiler.Default)
    epObjects.append(boiler)
    output_variable_name = "Boiler " + boiler.FuelType + " Energy"
    epObjects.append(Variable(
        Name = output_variable_name))

def GetWaterToAirHeatPumpObject(zone_name, zonelistName):
    return WaterToAirHeatPump(
        ZoneName = zone_name,
        TemplateThermostatName = f'Thermostat.{zonelistName}',
    )