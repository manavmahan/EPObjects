from Helper.Modules import *
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
    epObjects.append(Variable.get_variable(Name = "Zone Air System Sensible Heating Rate"))
    epObjects.append(Variable.get_variable(
        Name = "Zone Air System Sensible Cooling Rate"))
    epObjects.append(Variable.get_variable(
        Name = "Zone Water to Air Heat Pump Electricity Energy"))
    epObjects.append(Variable.get_variable(
        Name = "Cooling Tower Fan Electricity Energy"))

def AddHeatPumpsWithBoiler(epObjects):
    AddHeatPumps(epObjects)
    boiler = Boiler(Boiler.Default)
    epObjects.append(boiler)
    output_variable_name = "Boiler " + {'Electricity' if boiler.FuelType=='Electricity' else 'gas'} + " Energy"
    epObjects.append(Variable.get_variable(
        Name = output_variable_name))

def GetWaterToAirHeatPumpObject(zone, zonelistName):
    hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
    hvac.ZoneName = zone.Name
    hvac.TemplateThermostatName = f'Thermostat.{zonelistName}'
    return hvac