import re
from idf_object.hvactemplate.plant.boiler import Boiler
from idf_object.hvactemplate.zone.watertoairheatpump import WaterToAirHeatPump


def AdjustObjectVariables(epObjects, objectType, pattern, valueName, probabilisticParameters):
    try: selected = next(p for p in probabilisticParameters.index if re.fullmatch(pattern, p))
    except: return
    objs = list(x for x in epObjects if isinstance(x, objectType))
    for obj in objs:
        setattr(obj, valueName, probabilisticParameters[selected])

def SetBestMatchSystemParameter(p_parameters, ep_objects, ):
    AdjustObjectVariables(ep_objects, WaterToAirHeatPump, 'HeatingCOP.*', 'HeatPumpHeatingCoilGrossRatedCOP', p_parameters)
    AdjustObjectVariables(ep_objects, Boiler, 'BoilerEfficiency.*', 'Efficiency', p_parameters)