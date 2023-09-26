import re
from idf_object.zonelist import People, Lights, ElectricEquipment

def AdjustZoneListVariables(ep_objects, object_type, pattern, value_name, p_parameters):
    selected = list(p for p in p_parameters.index if re.fullmatch(pattern, p))
    objs = list(x for x in ep_objects if isinstance(x, object_type))
    for obj in objs:
        name = None
        for lookfor in (getattr(obj, 'ZoneListName'),):
            try:
                name = next(x for x in selected if lookfor in x)
                break
            except: pass
        if name is not None:
            setattr(obj, value_name, p_parameters[name])

def SetBestMatchInternalHeatGains(p_parameters, ep_objects, ):
    AdjustZoneListVariables(ep_objects, People, 'Occupancy.*', 'ZoneFloorAreaperPerson', p_parameters)
    AdjustZoneListVariables(ep_objects, Lights, 'LightHeatGain.*', 'WattsperZoneFloorArea', p_parameters)
    AdjustZoneListVariables(ep_objects, ElectricEquipment, 'EquipmentHeatGain.*', 'WattsperZoneFloorArea', p_parameters)
