import re
from IDFObject.Zone import Zone, Infiltration

def SetBestMatchPermeability(probabilisticParameters, epObjects):
    zones = list(x for x in epObjects if isinstance(x, Zone))
    external_surface_area = sum(x.ExternalSurfaceArea for x in zones)
    net_volume = sum(x.NetVolume for x in zones)
    
    selected = list(p for p in probabilisticParameters.index if re.fullmatch('Permeability.*', p))
    infiltrations = list(x for x in epObjects if isinstance(x, Infiltration))
    for infiltration in infiltrations:
        zone = next(x for x in epObjects if isinstance(x, Zone) and x.Name==infiltration.ZoneListName)
        for lookfor in (infiltration.ZoneListName, ''):
            try:
                name = next(x for x in selected if lookfor in x)
                break
            except: pass
        infiltration.AirChangesperHour = round(0.1 + (0.07 * probabilisticParameters[name] * (external_surface_area / net_volume)), 5)