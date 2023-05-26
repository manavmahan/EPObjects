import re
import copy

# Contruction
from IDFObject.Construction import Construction
from IDFObject.Material import Material
from IDFObject.WindowMaterial.SimpleGlazingSystem import SimpleGlazingSystem
from IDFObject.BuildingSurface.Detailed import Detailed as BuildingSurface
from IDFObject.FenestrationSurface.Detailed import Detailed as FenestrationSurface

def get_construction_names(ep_objects):
    construction_names = []
    for surface in ep_objects:
        if isinstance(surface, (BuildingSurface, FenestrationSurface, InternalMass)):
            if surface.ConstructionName not in construction_names:
                construction_names.append(surface.ConstructionName)
    return construction_names

def get_material_names(constructions):
    materials = dict()
    for construction in constructions:
        for material in construction.MaterialsName:
            split = material.split('.')
            try:
                materials['.'.join(split[:-1])] = float(split[-1])
            except ValueError:
                if material not in materials: materials[material] = None
    materials["RollShade"] = None
    return materials

def create_construction_materials(parameters, constructions, materials):
    constructions_copy = copy.deepcopy(constructions)
    materials_copy = copy.deepcopy(materials)
    for parameter in parameters.index:
        if not re.fullmatch('u-value.*', parameter): continue
        construction_name = parameter.split(':')[1]
        try: construction = next(x for x in constructions_copy if x.Name == construction_name)
        except StopIteration: raise KeyError(f"cannot find {construction_name}")
        construction.initialise_materials(materials_copy)

        g_value_parameter_name = parameter.replace('u-value', 'g-value')
        g_value = parameters.get(g_value_parameter_name, None)

        material = construction.adjust_properties(parameters[parameter], g_value)
        if material is not None: materials_copy.append(material)
    clean_materials(constructions_copy, materials_copy)
    constructions_copy += materials_copy
    return constructions_copy

def clean_materials(constructions, materials):
    material_names = get_material_names(constructions).keys()
    delete_objects = list(x for x in materials if x.Name not in material_names)
    for obj in delete_objects: materials.remove(obj)

from IDFObject.zonelist import Zonelist

# def set_best_match_construction(epObjects,):
#     surfaces = list(x for x in epObjects if isinstance(x, BuildingSurface))
#     fenestrations = list(x for x in epObjects if isinstance(x, FenestrationSurface))

#     constructions = list(x for x in epObjects if isinstance(x, Construction))
#     zoneLists = list(x for x in epObjects if isinstance(x, ZoneList)) 
#     for surface in surfaces:
#         try: zoneName = surface.ZoneName
#         except AttributeError: zoneName = next(x for x in surfaces if x.Name == surface.BuildingSurfaceName).ZoneName
#         try: zoneListName = next(x for x in zoneLists if zoneName in x.IDF).Name
#         except StopIteration: raise StopIteration(zoneName, [x.IDF for x in zoneLists])
#         selected = list(x for x in constructions if surface.ConstructionName in x.Name)
#         for lookfor in (surface.Name, zoneName, zoneListName, ''):
#             try:
#                 name = next(x for x in selected if lookfor in x.Name).Name
#                 break
#             except: name = None

#         if not name:
#             raise KeyError(f'Cannot find construction for {surface.Name} - {surface.ConstructionName} in {[x.Name for x in selected]}')
#         surface.ConstructionName = name

#         for fenestration in (x for x in fenestrations if x.BuildingSurfaceName == surface.Name):
#             selected = list(x for x in constructions if fenestration.ConstructionName in x.Name)
#             for lookfor in (fenestration.Name, zoneName, zoneListName, ''):
#                 try:
#                     name = next(x for x in selected if lookfor in x.Name).Name
#                     break
#                 except: pass
#             fenestration.ConstructionName = name



# Zone

from IDFObject.Zone import Zone, InternalMass

def SetBestMatchInternalMass(probabilisticParameters, epObjects, ):
    zones = list(x for x in epObjects if isinstance(x, Zone))
    zoneLists = list(x for x in epObjects if isinstance(x, Zonelist))
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