from Helper.Modules import *
from IDFObject.HVACTemplate.Plant.HotWaterLoop import HotWaterLoop
from IDFObject.HVACTemplate.Zone.BaseboardHeat import BaseboardHeat
from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump
from IDFObject.Output.Variable import Variable

def AddHeatPumps(epObjects):
    zones = list (x for x in epObjects if isinstance(x, Zone))
    zoneLists = list (x for x in epObjects if isinstance(x, ZoneList))
    for zone in zones:
        zoneListName = next(x for x in zoneLists if zone.Name in x.IDF).Name
        zoneWAHP = GetWaterToAirHeatPumpObject(zone, zoneListName)
        epObjects.append(zoneWAHP)

    epObjects.append(MixedWaterLoop(MixedWaterLoop.Default))
    epObjects.append(Tower(Tower.Default))
    epObjects.append(Variable(
        Name = "Zone Air System Sensible Heating Rate"))
    epObjects.append(Variable(
        Name = "Zone Air System Sensible Cooling Rate"))
    epObjects.append(Variable(
        Name = "Zone Water to Air Heat Pump Electricity Energy"))
    epObjects.append(Variable(
        Name = "Cooling Tower Fan Electricity Energy"))
    
def add_baseboard_heating(ep_objects, boiler_fuel_type="Gas"):
    zones = list (x for x in ep_objects if isinstance(x, Zone))
    zonelists = list (x for x in ep_objects if isinstance(x, ZoneList))
    for zone in zones:
        zonelist_name = next(x for x in zonelists if zone.Name in x.IDF).Name
        zone_bh = get_zone_baseboard_heating(zone, zonelist_name)
        ep_objects.append(zone_bh)

    ep_objects.append(Variable(
        Name = "Zone Air System Sensible Heating Rate"))

    ep_objects.append(HotWaterLoop.get_default())
    ep_objects.append(Boiler.get_default(
        FuelType = boiler_fuel_type
    ))
    output_variable_name = "Boiler " + {'Electricity' if boiler_fuel_type=='Electricity' else 'gas'} + " Energy"
    ep_objects.append(Variable(
        Name = output_variable_name))
    
    
def get_zone_baseboard_heating(zone, zonelist_name):
    bh = BaseboardHeat.get_default(
        Name = zone.Name,
        TemplateThermostatName = f'Thermostat.{zonelist_name}'
    )
    return bh

def AddHeatPumpsWithBoiler(epObjects):
    AddHeatPumps(epObjects)
    boiler = Boiler(Boiler.Default)
    epObjects.append(boiler)
    output_variable_name = "Boiler " + {'Electricity' if boiler.FuelType=='Electricity' else 'gas'} + " Energy"
    epObjects.append(Variable(
        Name = output_variable_name))

def GetWaterToAirHeatPumpObject(zone, zonelistName):
    hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
    hvac.ZoneName = zone.Name
    hvac.TemplateThermostatName = f'Thermostat.{zonelistName}'
    return hvac