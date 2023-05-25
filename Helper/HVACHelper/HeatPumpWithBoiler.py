from Helper.Modules import *
from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump
from IDFObject.Output.Variable import Variable

def add_heat_pumps(epObjects):
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

def AddHeatPumpsWithBoiler(epObjects):
    add_heat_pumps(epObjects)
    boiler = Boiler(Boiler.Default)
    epObjects.append(boiler)
    output_variable_name = "Boiler " + boiler.FuelType + " Energy"
    epObjects.append(Variable(
        Name = output_variable_name))

def GetWaterToAirHeatPumpObject(zone, zonelistName):
    return WaterToAirHeatPump(
        ZoneName = zone.Name,
        TemplateThermostatName = f'Thermostat.{zonelistName}',
    )