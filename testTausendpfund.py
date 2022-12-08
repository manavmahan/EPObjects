import math
import numpy as np

from ListObject import ListObject

from GeometryObject.XYZList import XYZList
from GeometryObject.Wall import CreateWallsByPointsHeightAndFloorCount, CreateFenestration, CreateFloors, CreateRoof

from IDFObject.Construction import Construction

from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump

from IDFObject.People import People

from IDFObject.Zone import Zone
from IDFObject.ZoneList import ZoneList

from Initialiser import InitialiseObject


epObjects = []

for obj in [
    "Version",
    "Building",
    'RunPeriod',
    "ConvergenceLimits",
    "GlobalGeometryRules",

    "Material",
    "WindowMaterial:SimpleGlazingSystem",

    "Schedule:Compact",
    "SimulationControl",
    "Site:GroundTemperature:BuildingSurface",
    "Site:Location",
    "SizingPeriod:WeatherFileDays",
    
    ]:
    epObjects += InitialiseObject('Data', obj)

for cons in [
    'ExternalWall',
    'FloorCeiling',
    'GroundFloor',
    'Roof',
    'Glazing',
    'InternalWall',
]:
    epObjects += [Construction(getattr(Construction, cons))]


officeZoneList = ZoneList(dict(Name = "Office", ZoneNames = ListObject()))
epObjects += [officeZoneList]
for i in range(3):
    epObjects += [Zone(dict(Name = f'Office.{i}.0'))]
    officeZoneList.AddZone (f'Office.{i}.0')

points = XYZList(np.array(((0,0,0), (14.7,0,0), (14.7,27,0), (0,27,0))))
# points.Rotate(math.pi/6)
points.DisplaceToOrigin()

epObjects += CreateFloors(points, 3.1, 3)
walls = CreateWallsByPointsHeightAndFloorCount(points, 3.1, 3)

epObjects += walls

for w in walls:
    epObjects += list( CreateFenestration(w, 0.3) )

epObjects += CreateRoof (points, 3.1, 3)

people = People(getattr(People, "Default"))
people.Name = "Office"
people.ZoneListName = "Office"
epObjects += [people]


epObjects += InitialiseObject('Data', "HVACTemplate:Thermostat")
epObjects += InitialiseObject('Data', "HVACTemplate:Plant:MixedWaterLoop",)
epObjects += InitialiseObject('Data', "HVACTemplate:Plant:Boiler",)
epObjects += InitialiseObject('Data', "HVACTemplate:Plant:Tower",)

for z in officeZoneList.ZoneNames.Values:
    hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
    hvac.ZoneName = z
    hvac.TemplateThermostatName = "Office"
    epObjects += [hvac]

for obj in [
    "Output:Diagnostics",
    "Output:Surfaces:Drawing",
    "Output:Variable",
]:
    epObjects += InitialiseObject('Data', obj)

print ('\n'.join([str(obj) for obj in epObjects]))