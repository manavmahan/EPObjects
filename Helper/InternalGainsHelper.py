import re

# Contruction
from Helper.Modules import People, ZoneList
from IDFObject.Material import Material
from IDFObject.WindowMaterial.SimpleGlazingSystem import SimpleGlazingSystem

def CreatePeople(probabilisticParameters, epObjects):
    for parameter in probabilisticParameters.index:
        if not re.fullmatch('People.*', parameter): continue
        name = parameter.split(':')[1]

        try:
            zonelist = next(x for x in epObjects if isinstance(x, ZoneList) and x.Name == name)
            epObjects.insert(0, zonelist.GetPeopleObject(probabilisticParameters[parameter]))
        except:
            zone = next(x for x in epObjects if isinstance(x, Zone) and x.Name == name)
            epObjects.insert(0, zone.GetPeopleObject(probabilisticParameters[parameter]))
# Surface

from IDFObject.BuildingSurface.Detailed import Detailed as BuildingSurface
from IDFObject.FenestrationSurface.Detailed import Detailed as FenestrationSurface
from IDFObject.ZoneList import ZoneList

def SetBestMatchConstruction(epObjects,):
    surfaces = list(x for x in epObjects if isinstance(x, BuildingSurface))
    fenestrations = list(x for x in epObjects if isinstance(x, FenestrationSurface))

    constructions = list(x for x in epObjects if isinstance(x, Construction))
    zoneLists = list(x for x in epObjects if isinstance(x, ZoneList)) 
    for surface in surfaces:
        try: zoneName = surface.ZoneName
        except: zoneName = next(x for x in surfaces if x.Name == surface.BuildingSurfaceName).ZoneName
        zoneListName = next(x for x in zoneLists if zoneName in x.IDF).Name
        selected = list(x for x in constructions if surface.ConstructionName in x.Name)
        for lookfor in (surface.Name, zoneName, zoneListName, ''):
            try:
                name = next(x for x in selected if lookfor in x.Name).Name
                break
            except: pass
        surface.ConstructionName = name

        for fenestration in (x for x in fenestrations if x.BuildingSurfaceName == surface.Name):
            selected = list(x for x in constructions if fenestration.ConstructionName in x.Name)
            for lookfor in (fenestration.Name, zoneName, zoneListName, ''):
                try:
                    name = next(x for x in selected if lookfor in x.Name).Name
                    break
                except: pass
            fenestration.ConstructionName = name

# Zone

from IDFObject.Zone import Zone

def GetExternalSurfaceArea(epObjects):
    return sum([x.ExternalSurfaceArea for x in epObjects if isinstance(x, Zone)])

def InitialiseZoneSurfaces(epObjects):
    surfaces = [x for x in epObjects if isinstance(x, BuildingSurface)]
    fenestrations = [x for x in epObjects if isinstance(x, FenestrationSurface)]
    for zone in [x for x in epObjects if isinstance(x, Zone)]:
        zone.AddSurfaces(surfaces, fenestrations)

def SetInternalMass(epObjects, massPerSqM=30):
    massMaterial = next(x for x in epObjects if isinstance(x, Material) and x.Name=="Mass")
    massOfInternalMaterial = massMaterial.Thickness * massMaterial.Density * massMaterial.SpecificHeat / 1000
    for zone in [x for x in epObjects if isinstance(x, Zone)]:
        epObjects += zone.GenerateInternalMass(massPerSqM, massOfInternalMaterial)

from IDFObject.Output.Variable import Variable
from EnumTypes import Frequency

def SetReportingFrequency(epObjects, frequency):
    variables = [x for x in epObjects if isinstance(x, Variable)]
    for v in variables:
        v.ReportingFrequency = frequency.name