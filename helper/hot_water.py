import re
from idf_object.wateruse.equipment import Equipment

def AdjustHotWaterVariables(ep_objects, object_type, pattern, value_name, p_parameters):
    try:
        selected = next(p for p in p_parameters.index if re.fullmatch(pattern, p))
        obj = next(x for x in ep_objects if isinstance(x, object_type))
        setattr(obj, value_name, p_parameters[selected]/(0.001*24*3600*1000))
    except StopIteration: pass

def set_hot_water_rate(p_parameters, ep_objects):
    AdjustHotWaterVariables(ep_objects, Equipment, 'HotWater.*', 'PeakFlowRate', p_parameters)