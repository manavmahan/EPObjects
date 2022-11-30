
from EnumTypes import SurfaceType
from IDFObject.Zone import Zone
from IDFObject.Daylighting import ReferencePoint

class Controls:
    __IDFName__ = "Daylighting"
    Properties = [
        'Name',
        'ZoneName',
    ]
    Name: str
    ZoneName: str

    def __init__(self, zone: Zone):
        self.Name = f"Daylighting.{self.__class__.__name__}.{zone.Name}"
        self.ZoneName = zone.Name

    def CreateDayLightReferencePoint(self, zone: Zone):
        for xyzs in [x.XYZs for x in zone.Surfaces if x.SurfaceType==SurfaceType.Floor]:
            pass
