from Helper.Modules import *
from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump

def AddHeatPumps(epObjects):
    zones = list (x for x in epObjects if isinstance(x, Zone))
    zoneLists = list (x for x in epObjects if isinstance(x, ZoneList))
    for zone in zones:
        zoneListName = next(x for x in zoneLists if zone.Name in x.IDF).Name
        zoneWAHP = GetWaterToAirHeatPumpObject(zone, zoneListName)
        epObjects.append(zoneWAHP)

    epObjects.append(MixedWaterLoop(MixedWaterLoop.Default))
    epObjects.append(Tower(Tower.Default))

def AddHeatPumpsWithBoiler(epObjects):
    AddHeatPumps(epObjects)
    epObjects.append(Boiler(Boiler.Default))

def GetWaterToAirHeatPumpObject(zone, zonelistName):
    hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
    hvac.ZoneName = zone.Name
    hvac.TemplateThermostatName = f'Thermostat.{zonelistName}'
    return hvac