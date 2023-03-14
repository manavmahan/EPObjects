from IDFObject.ZoneList import People

def AdjustZoneListVariables(epObjects, objectType, valueName, probabilisticParameters):
    pattern = f'{objectType.__name__}.*'
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

def SetBestMatchPeople(epObjects, probabilisticParameters):
    AdjustZoneListVariables(epObjects, People, 'ZoneFloorAreaperPerson', probabilisticParameters)
