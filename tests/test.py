from helper.surfaces_by_floor_points import CreatelWallsByPointsAndHeight, CreateFenestration
from idf_object.idfobject import IDFObject, IDFJsonEncoder, IDFJsonDecoder

from geometry_object.xyzlist import XYZList
import json 

points = XYZList("4,0,16,0,0,27,0,6,27,0,6,16,0")
print (points)

walls = CreatelWallsByPointsAndHeight(points, 3.25, 'Office.0.1')
print (json.dumps(walls, cls=IDFJsonEncoder))
print ([json.dumps(list(y), cls=IDFJsonEncoder) for y in [CreateFenestration(x, 0.4) for  x in walls]])