import math
from IDFObject.Zone import Zone
from EnumTypes import SurfaceType

def check_surfaces_cardinality(zone: Zone):
    messages = []
    for surface in zone.Surfaces:
        xyzs = surface.XYZs
        outside_point = xyzs.get_point_on_postive_zside()

        if surface.SurfaceType==SurfaceType.Floor:
            if xyzs.XYZs[0, 2] < outside_point[2]: 
                messages.append(ValueError(f'Floor {surface.IDF} not arranged counter clockwise.'))
                surface.XYZs = surface.XYZs.Flip()
        elif surface.SurfaceType==SurfaceType.Ceiling or surface.SurfaceType==SurfaceType.Roof:
            if xyzs.XYZs[0, 2] > outside_point[2]: 
                messages.append(ValueError(f'Roof/Ceiling {surface.IDF} not arranged counter clockwise.'))
                surface.XYZs = surface.XYZs.Flip()
        else:
            if any(x.XYZs.is_inside(outside_point) for x in zone.Surfaces if x.SurfaceType==SurfaceType.Floor): 
                messages.append(ValueError(f'Wall {surface.IDF} not arranged counter clockwise.'))
                surface.XYZs = surface.XYZs.Flip()
            
            for fen in surface.Fenestrations:
                if abs(surface.XYZs.plane.angle_from_xaxis - fen.XYZs.plane.angle_from_xaxis) > math.pi/2:
                    messages.append(ValueError(f'Fenestration {fen.IDF} not arranged counter clockwise.'))
                    fen.XYZs = fen.XYZs.Flip()
    return messages