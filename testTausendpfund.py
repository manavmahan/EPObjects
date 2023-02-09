import json

from IDFObject.BuildingSurface.Detailed import Detailed as BuildingSurface
from IDFObject.Construction import Construction
from IDFObject.ConvergenceLimits import ConvergenceLimits
from IDFObject.ElectricEquipment import ElectricEquipment
from IDFObject.FenestrationSurface.Detailed import Detailed as FenestrationSurface
from IDFObject.GlobalGeometryRules import GlobalGeometryRules
from IDFObject.HVACTemplate.Plant.Boiler import Boiler
from IDFObject.HVACTemplate.Plant.MixedWaterLoop import MixedWaterLoop
from IDFObject.HVACTemplate.Plant.Tower import Tower
from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump
from IDFObject.HVACTemplate.Thermostat import Thermostat
from IDFObject.Material import Material
from IDFObject.Output.Surfaces.Drawing import Drawing
from IDFObject.Output.Table.SummaryReports import SummaryReports
from IDFObject.Output.Diagnostics import Diagnostics
from IDFObject.Output.PreprocessorMessage import PreprocessorMessage
from IDFObject.Output.Variable import Variable
from IDFObject.Output.VariableDictionary import VariableDictionary
from IDFObject.OutputControl.Table.Style import Style
from IDFObject.RunPeriod import RunPeriod
from IDFObject.Schedule.Compact import Compact
from IDFObject.ScheduleTypeLimits import ScheduleTypeLimits
from IDFObject.SimulationControl import SimulationControl
from IDFObject.Site.GroundTemperature.BuildingSurface import BuildingSurface
from IDFObject.Site.Location import Location
from IDFObject.SizingPeriod.WeatherFileDays import WeatherFileDays
from IDFObject.Timestep import Timestep
from IDFObject.Version import Version
from IDFObject.WindowMaterial.Shade import Shade
from IDFObject.WindowMaterial.SimpleGlazingSystem import SimpleGlazingSystem
from IDFObject.Zone import Zone
from IDFObject.ZoneInfiltration.DesignFlowRate import DesignFlowRate
from IDFObject.ZoneList import ZoneList

from IDFObject.IDFObject import IDFObject, IDFJsonEncoder, IDFJsonDecoder

with open('Test/Tausendpfund.json') as f:
    epObjects = json.load(f, cls=IDFJsonDecoder)

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
    insulationLayer = cons.AdjustUValue(constructions[construction])
    if insulationLayer: 
        epObjects += [insulationLayer[0]]

    if construction == "Glazing":
        cons.AdjustGValue(0.35)
    epObjects += [cons]

zoneLists = list(x for x in epObjects if isinstance(x, (ZoneList)))

surfaces = [x for x in epObjects if isinstance(x, BuildingSurface)]
fenestrations = [x for x in epObjects if isinstance(x, FenestrationSurface)]

massMaterial = next(x for x in epObjects if isinstance(x, Material) and x.Name=="Mass")
massOfInternalMaterial = massMaterial.Thickness * massMaterial.Density * massMaterial.SpecificHeat / 1000

for zone in [x for x in epObjects if isinstance(x, Zone)]:
    zone.AddSurfaces(surfaces, fenestrations)
    epObjects += zone.GenerateInternalMass(60, massOfInternalMaterial)

externalSurfaceArea = sum([x.ExternalSurfaceArea for x in epObjects if isinstance(x, Zone)])
netVolume = sum([x.NetVolume for x in epObjects if isinstance(x, Zone)])
ach = round(0.1 + 0.07 * 6 * externalSurfaceArea / (0.8 * netVolume), 5)

for zoneList in zoneLists:
    epObjects += [zoneList.GetPeopleObject(20)]
    epObjects += [zoneList.GetLightsObject(6)]
    epObjects += [zoneList.GetElectricEquipmentObject(10)]
    epObjects += [zoneList.GetInfiltrationObject(ach)]
    epObjects += [zoneList.GetDefaultVentilationObject()]
    epObjects += [zoneList.GetNaturalVentilationObject()]

for zone in [x for x in epObjects if isinstance(x, Zone)]:
    hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
    hvac.ZoneName = zone.Name
    hvac.TemplateThermostatName = "Office"
    epObjects += [hvac]

# print ('\n'.join([str(obj) for obj in epObjects]))
# print ('\n'.join([str(obj) for obj in epObjects]))

for x in epObjects:
    # if isinstance(x, BuildingSurface):

    s = json.dumps(x, cls=IDFJsonEncoder)
    o = json.loads(s, cls=IDFJsonDecoder)
    print (o.IDF,)
    
    # break
    # print (Zone(json.loads(str)))