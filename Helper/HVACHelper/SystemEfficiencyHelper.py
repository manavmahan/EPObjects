import re
from IDFObject.HVACTemplate.Zone.WaterToAirHeatPump import WaterToAirHeatPump


def AdjustObjectVariables(epObjects, objectType, pattern, valueName, probabilisticParameters):
    try: selected = next(p for p in probabilisticParameters.index if re.fullmatch(pattern, p))
    except: return
    objs = list(x for x in epObjects if isinstance(x, objectType))
    for obj in objs:
        setattr(obj, valueName, probabilisticParameters[selected])

def SetBestMatchSystemParameter(probabilisticParameters, epObjects, ):
    AdjustObjectVariables(epObjects, WaterToAirHeatPump, 'HeatingCOP.*', 'HeatPumpHeatingCoilGrossRatedCOP', probabilisticParameters)