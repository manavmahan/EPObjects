import json
import math
import numpy as np

from ListObject import ListObject

from GeometryObject.XYZList import XYZList

from GeometryObject.Wall import CreateWallsByPointsHeightAndFloorCount, CreateFenestration, CreateFloors, CreateRoof

from IDFObject.BuildingSurface.Detailed import Detailed as BuildingSurface

from IDFObject.FenestrationSurface.Detailed import Detailed as FenestrationSurface

from IDFObject.Construction import Construction

from IDFObject.ElectricEquipment import ElectricEquipment

from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump

from IDFObject.IDFObject import IDFObject, IDFJsonEncoder, IDFJsonDecoder

from IDFObject.Material import Material

from IDFObject.Version import Version

from IDFObject.WindowMaterial.SimpleGlazingSystem import SimpleGlazingSystem

from IDFObject.Zone import Zone

from IDFObject.ZoneInfiltration.DesignFlowRate import DesignFlowRate

from IDFObject.ZoneList import ZoneList

from Initialiser import InitialiseObject


epObjects = []

for obj in [
    "Version",
    "Building",
    'RunPeriod',
    'Timestep',
    "ConvergenceLimits",
    "GlobalGeometryRules",

    "Material",
    "WindowMaterial:SimpleGlazingSystem",
    "WindowMaterial:Shade",

    "Schedule:Compact",
    "SimulationControl",
    "Site:GroundTemperature:BuildingSurface",
    "Site:Location",
    "SizingPeriod:WeatherFileDays",
]:
    epObjects += InitialiseObject('Data', obj)

materials = list(x for x in epObjects if isinstance(x, (Material, SimpleGlazingSystem)))

constructions = {
    'ExternalWall': 0.18,
    'FloorCeiling': 0.4,
    'GroundFloor': 0.18,
    'Roof': 0.15,
    'Glazing': 0.87,
    'InternalWall': 0.4,
    'Mass': None,
}
for construction in constructions:
    cons = Construction(getattr(Construction, construction), materials)
    insulationLayer = cons.AdjustUValue(constructions[construction], "Insulation")
    if construction == "Glazing":
        cons.AdjustGValue(0.35)
    if insulationLayer: epObjects += [insulationLayer]
    epObjects += [cons]

officeZoneList = ZoneList(dict(Name = "Office", ZoneNames = ListObject()))
epObjects += [officeZoneList]
for i in range(3):
    epObjects += [Zone(dict(Name = f'Office.{i}.0'))]
    officeZoneList.AddZone (f'Office.{i}.0')

points = XYZList(np.array(((0,0,0), (14.7,0,0), (14.7,27,0), (0,27,0))))
points.Rotate(math.pi/6)
points.DisplaceToOrigin()

epObjects += CreateFloors(points, 3.1, 3)
walls = CreateWallsByPointsHeightAndFloorCount(points, 3.1, 3)

epObjects += walls

for w in walls:
    epObjects += list( CreateFenestration(w, 0.33) )

epObjects += CreateRoof (points, 3.1, 3)

surfaces = [x for x in epObjects if isinstance(x, BuildingSurface)]
fenestrations = [x for x in epObjects if isinstance(x, FenestrationSurface)]

massMaterial = next(x for x in epObjects if isinstance(x, Material) and x.Name=="Mass")
massOfInternalMaterial = massMaterial.Thickness * massMaterial.Density * massMaterial.SpecificHeat / 1000

for zone in [x for x in epObjects if isinstance(x, Zone)]:
    zone.AddSurfaces(surfaces, fenestrations)
    epObjects += zone.GenerateDaylightControl('Office')
    epObjects += zone.GenerateWindowShadingControl()
    epObjects += zone.GenerateInternalMass(60, massOfInternalMaterial)

epObjects += [officeZoneList.GetPeopleObject(20)]
epObjects += [officeZoneList.GetLightsObject(6)]
epObjects += [officeZoneList.GetElectricEquipmentObject(10)]

externalSurfaceArea = sum([x.ExternalSurfaceArea for x in epObjects if isinstance(x, Zone)])
netVolume = sum([x.NetVolume for x in epObjects if isinstance(x, Zone)])
ach = round(0.1 + 0.07 * 6 * externalSurfaceArea / (0.8 * netVolume), 5)

epObjects += [officeZoneList.GetInfiltrationObject(ach)]
epObjects += [officeZoneList.GetDefaultVentilationObject()]
epObjects += [officeZoneList.GetNaturalVentilationObject()]

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
    "OutputControl:Table:Style",
    "Output:Diagnostics",
    "Output:Surfaces:Drawing",
    "Output:Variable",
]:
    epObjects += InitialiseObject('Data', obj)

# print ('\n'.join([str(obj) for obj in epObjects]))
# print ('\n'.join([str(obj) for obj in epObjects]))

import json

zone = next(x for x in epObjects if isinstance(x, Zone))

for x in epObjects:
    # if isinstance(x, BuildingSurface):

    s = json.dumps(x, cls=IDFJsonEncoder)
    o = json.loads(s, cls=IDFJsonDecoder)
    print (o.IDF,)
    
    # break
    # print (Zone(json.loads(str)))