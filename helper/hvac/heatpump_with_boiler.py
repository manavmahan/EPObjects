from helper.hvac import get_zonelists_with_thermostat
from idf_object.hvactemplate.thermostat import Thermostat
from idf_object.hvactemplate.zone.watertoairheatpump import WaterToAirHeatPump
from idf_object.hvactemplate.plant.boiler import Boiler
from idf_object.hvactemplate.plant.mixedwaterloop import MixedWaterLoop
from idf_object.hvactemplate.plant.tower import Tower
from idf_object.output.variable import Variable
from idf_object.zonelist import ZoneList

def add_heatpumps(ep_objects):
    thermostats = list (x for x in ep_objects if isinstance(x, Thermostat))
    zonelists = list (x for x in ep_objects if isinstance(x, ZoneList))

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