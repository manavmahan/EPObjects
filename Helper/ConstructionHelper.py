import re

# Contruction
from IDFObject.Construction import Construction
from IDFObject.Material import Material
from IDFObject.WindowMaterial.SimpleGlazingSystem import SimpleGlazingSystem
from IDFObject.BuildingSurface.Detailed import Detailed as BS
from IDFObject.FenestrationSurface.Detailed import Detailed as FS

def get_construction_names(ep_objects):
    for surface in ep_objects:
        if isinstance(surface, (BS, FS)):
            yield surface.ConstructionName

def get_material_names(ep_objects):
    for construction in ep_objects:
        if isinstance(construction, (Construction)):
            for m in construction.MaterialsName.Values:
                split = m.split('.')
                try:
                    thickness = float(split[-1])
                    material_name = '.'.join(split[:-1])
                except ValueError:
                    thickness = None
                    material_name = m
                yield (material_name, thickness)

def create_constructions(parameter_set, ep_objects):
    materials = list(x for x in ep_objects if isinstance(x, (Material, SimpleGlazingSystem)))
    constructions = list(x for x in ep_objects if isinstance(x, (Construction)))
    for parameter in parameter_set.index:
        if not re.fullmatch('u-value.*', parameter): continue
        try: base_construction = next(x for x in constructions if x.Name == parameter.split(':')[1])
        except StopIteration: raise KeyError(f"cannot find {parameter.split(':')[1]}")
        new_construction = Construction(**dict(base_construction.ToDict()))
        new_construction.Name = parameter

        new_construction.initialise_materials(materials)

        g_value_parameter_name = parameter.replace('u-value', 'g-value')
        g_value = parameter_set[g_value_parameter_name] if g_value_parameter_name in parameter_set else None

        material = new_construction.AdjustProperties(parameter_set[parameter], g_value)
        if material is not None: 
            ep_objects.append(material)
        ep_objects.append(new_construction)

def clean_construction_materials(ep_objects):
    construction_names = set(x.ConstructionName for x in ep_objects if isinstance(x, (BuildingSurface, FenestrationSurface, InternalMass)))
    material_names = []

    delete_objects = list(x for x in ep_objects if isinstance(x, Construction) and x.Name not in construction_names)
    for obj in delete_objects: ep_objects.remove(obj)
    for x in ep_objects:
        if isinstance(x, Construction):
            material_names += x.MaterialsName.Values
    material_names = set(material_names)

    delete_objects = list(x for x in ep_objects if isinstance(x, (Material, SimpleGlazingSystem)) and x.Name not in material_names)
    for obj in delete_objects: ep_objects.remove(obj)

    constructions = list(x.Name for x in ep_objects if isinstance(x, (Construction)))
    materials = list(x.Name for x in ep_objects if isinstance(x, (Material, SimpleGlazingSystem)))
    for x in construction_names:
        if x not in constructions: raise KeyError("error initialising construction: {x}")
    for x in material_names:
        if x not in materials: raise KeyError("error initialising material: {x}")

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
        except AttributeError: zoneName = next(x for x in surfaces if x.Name == surface.BuildingSurfaceName).ZoneName
        try: zoneListName = next(x for x in zoneLists if zoneName in x.IDF).Name
        except StopIteration: raise StopIteration(zoneName, [x.IDF for x in zoneLists])
        selected = list(x for x in constructions if surface.ConstructionName in x.Name)
        for lookfor in (surface.Name, zoneName, zoneListName, ''):
            try:
                name = next(x for x in selected if lookfor in x.Name).Name
                break
            except: name = None

        if not name:
            raise KeyError(f'Cannot find construction for {surface.Name} - {surface.ConstructionName} in {[x.Name for x in selected]}')
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

from IDFObject.Zone import Zone, InternalMass

def SetBestMatchInternalMass(probabilisticParameters, epObjects, ):
    zones = list(x for x in epObjects if isinstance(x, Zone))
    zoneLists = list(x for x in epObjects if isinstance(x, ZoneList))
    masses = list(x for x in epObjects if isinstance(x, InternalMass))

    massMaterial = next(x for x in epObjects if isinstance(x, Material) and x.Name=="Mass")
    massOfInternalMaterial = massMaterial.Thickness * massMaterial.Density * massMaterial.SpecificHeat / 1000

    selected = list(x for x in probabilisticParameters.index if re.fullmatch('InternalMass.*', x))
    for zone in zones:
        try: massObj = next(x for x in epObjects)
        except: continue
        zoneListName = next(x for x in zoneLists if zone.Name in x.IDF).Name
        name = None
        for lookfor in (zone.Name, zoneListName, ''):
            try:
                name = next(x for x in selected if lookfor in x.Name).Name
                break
            except: pass
        if name: massObj.SurfaceArea = zone.FloorArea * probabilisticParameters[name] / massOfInternalMaterial,

def GetExternalSurfaceArea(epObjects):
    return sum([x.ExternalSurfaceArea for x in epObjects if isinstance(x, Zone)])

def InitialiseZoneSurfaces(epObjects):
    surfaces = [x for x in epObjects if isinstance(x, BuildingSurface)]
    fenestrations = [x for x in epObjects if isinstance(x, FenestrationSurface)]
    for zone in [x for x in epObjects if isinstance(x, Zone)]:
        zone.AddSurfaces(surfaces, fenestrations)

def set_internal_mass(epObjects, massPerSqM=30):
    massMaterial = next(x for x in epObjects if isinstance(x, Material) and x.Name=="Mass")
    massOfInternalMaterial = massMaterial.Thickness * massMaterial.Density * massMaterial.SpecificHeat / 1000
    for zone in [x for x in epObjects if isinstance(x, Zone)]:
        epObjects.append(zone.GenerateInternalMass(massPerSqM, massOfInternalMaterial))

from IDFObject.Output.Variable import Variable
from EnumTypes import Frequency

def set_reporting_frequency(epObjects, frequency):
    variables = [x for x in epObjects if isinstance(x, Variable)]
    for v in variables:
        v.ReportingFrequency = frequency.name