from IDFObject.HeatPump.PlantLoop.EIR.Heating import Heating
from IDFObject.ZoneHVAC.EquipmentConnections import EquipmentConnections
from IDFObject.ZoneHVAC.EquipmentList import EquipmentList
from IDFObject.ZoneHVAC.LowTemperatureRadiant.VariableFlow import VariableFlow
from IDFObject.ZoneHVAC.LowTemperatureRadiant.VF.Design import Design

from IDFObject.ConstructionProperty.InternalHeatSource import InternalHeatSource
from IDFObject.Construction import Construction

from IDFObject.Curve.Biquadratic import Biquadratic
from IDFObject.Curve.Quadratic import Quadratic

from EnumTypes import SurfaceType
from IDFObject.BuildingSurface.Detailed import Detailed
from IDFObject.Zone import Zone
from IDFObject.zonelist import Zonelist
from IDFObject.ZoneControl.Thermostat import Thermostat
from IDFObject.ThermostatSetpoint.SingleHeating import SingleHeating
from IDFObject.ThermostatSetpoint.SingleCooling import SingleCooling
from IDFObject.Schedule.Compact import Compact
from IDFObject.Schedule.File import File

def GetCompleteSystemObjects(epObjects):
    h = Heating(Heating.Default)
    c1 = Biquadratic(Biquadratic.HPHeatingCAPFTemp)
    c2 = Biquadratic(Biquadratic.HPHeatingEIRFTemp)
    c3 = Quadratic(Quadratic.HPHeatPLFFPLR)
    h.HPHeatingCAPFTemp = c1.Name
    h.HPHeatingEIRFTemp = c2.Name
    h.HPHeatPLFFPLR = c3.Name
    return GetUnderfloorSystemForZones(epObjects) + [h, c1, c2, c3]

def GetUnderfloorSystemForZones(epObjects):
    zones = list(x for x in epObjects if isinstance(x, Zone))
    surfaces = list(x for x in epObjects if isinstance(x, Detailed) and x.SurfaceType==SurfaceType.Floor)

    objs = []
    for zone in zones:
        floor = next (s for s in surfaces if s.ZoneName==zone.Name)
        d = Design(Design.Default)
        d.Name = f'{floor.Name}-DesignUnderfloorHeating'
        
        v = VariableFlow(VariableFlow.Default)
        v.Name = f'{zone.Name}-UnderfloorHeating'
        v.DesignObjectName = d.Name
        v.ZoneName = zone.Name
        v.SurfaceNameorRadiantSurfaceGroupName = floor.Name

        e = EquipmentList(EquipmentList.Default)
        e.Name = f'{zone.Name}-Equipment'
        e.ZoneEquipment1ObjectType = v.__IDFName__
        e.ZoneEquipment1Name = v.Name

        c = EquipmentConnections(EquipmentConnections.Default)
        c.ZoneName = zone.Name
        c.ListNameZoneEquipment = e.Name
        c.ZoneAirNodeName = f'{zone.Name} Air Node'
        c.ZoneReturnAirNodeorNodeListName = f'{zone.Name} Return Air Node'
        objs += [d, v, e, c]
    return objs

def AddRadiatPropertyToConstruction(epObjects):
    surfaces = list(x for x in epObjects if isinstance(x, Detailed) and x.SurfaceType==SurfaceType.Floor)

    try:
        radiantSurfacesName = list(x.SurfaceNameorRadiantSurfaceGroupName for x in epObjects if isinstance(x, VariableFlow))
    except:
        return

    constructionProperties = list(x.SurfaceNameorRadiantSurfaceGroupName for x in epObjects if isinstance(x, InternalHeatSource))
    constructions = list(x for x in epObjects if isinstance(x, Construction))

    for radiantSurfaceName in radiantSurfacesName:
        surface = next(s for s in surfaces if s.Name==radiantSurfaceName)
        constructionName = surface.ConstructionName
        try:
            internalHeatSource = next(c for c in constructionProperties if c.ConstructionName==constructionName)
            continue
        except:
            newProperty = InternalHeatSource(InternalHeatSource.Floor)
            newProperty.Name = f"FloorSource-{constructionName}"
            newProperty.ConstructionName = constructionName
            construction = next(c for c in constructions if c.Name==constructionName)
            newProperty.ThermalSourcePresentAfterLayerNumber = len(construction.MaterialsName.Values) - 2
            newProperty.TemperatureCalculationRequestedAfterLayerNumber = newProperty.ThermalSourcePresentAfterLayerNumber + 1
            constructionProperties += [newProperty]
            epObjects += [newProperty]


def AddZoneListControls(epObjects,):
    zoneLists = list(x for x in epObjects if isinstance(x, Zonelist))
    schedule = next(x for x in epObjects if isinstance(x, Compact) and x.Name=="HeatingCoolingSeason")
    
    schedules = list(x for x in epObjects if isinstance(x, File))

    for zoneList in zoneLists:
        c1 = SingleHeating(dict())
        c1.Name = f'Heating Setpoint with SB - {zoneList.Name}'
        c1.SetpointTemperatureScheduleName = next(s for s in schedules if s.Name==f"{zoneList.Name}.HeatingSetPoint").Name

        c2 = SingleCooling(dict())
        c2.Name = f'Cooling Setpoint with SB - {zoneList.Name}'
        c2.SetpointTemperatureScheduleName = next(s for s in schedules if s.Name==f"{zoneList.Name}.CoolingSetPoint").Name

        t = Thermostat(Thermostat.Default)
        t.Name = f'Thermostat-{zoneList.Name}'
        t.ZoneorZoneListName = zoneList.Name
        t.ControlTypeScheduleName = schedule.Name
        t.Control1Name = c1.Name
        t.Control2Name = c2.Name

        epObjects += [c1, c2, t]