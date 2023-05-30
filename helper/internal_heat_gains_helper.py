import re
from idf_object.zonelist import People, Lights, ElectricEquipment

def AdjustZoneListVariables(epObjects, objectType, pattern, valueName, probabilisticParameters):
    selected = list(p for p in probabilisticParameters.index if re.fullmatch(pattern, p))
    objs = list(x for x in epObjects if isinstance(x, objectType))
    for obj in objs:
        name = None
        for lookfor in (getattr(obj, 'ZoneListName'),):
            try:
                name = next(x for x in selected if lookfor in x)
                break
            except: pass
        if name is not None:
            setattr(obj, valueName, probabilisticParameters[name])

def SetBestMatchInternalHeatGains(probabilisticParameters, epObjects, ):
    AdjustZoneListVariables(epObjects, People, 'Occupancy.*', 'ZoneFloorAreaperPerson', probabilisticParameters)
    AdjustZoneListVariables(epObjects, Lights, 'LightHeatGain.*', 'WattsperZoneFloorArea', probabilisticParameters)
    AdjustZoneListVariables(epObjects, ElectricEquipment, 'EquipmentHeatGain.*', 'WattsperZoneFloorArea', probabilisticParameters)
