import BuildingSurface

from ..EnumTypes import SurfaceType

class Zone:
    __IDFName__ = "Zone"
    Properties = {
        "Name": None,
    }
    
    Surfaces = list()

    __ceilingArea = 0
    __floorArea = 0
    __wallArea = 0
    __windowArea = 0
    __roofArea = 0

    __surfaces = list()
    @property
    def Surfaces(self): return self.__surfaces

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties.keys(), properties)

    def AddSurface(self, surface: BuildingSurface.Detailed) -> None:
        if surface.Area == None | 0:
            raise Exception(f"Cannot add surface without area {surface}.")

        match surface.Type:
            case SurfaceType.Ceiling:
                self.__ceilingArea += surface.Area

            case SurfaceType.Floor:
                self.__floorArea += surface.Area
            
            case SurfaceType.Roof:
                self.__roofArea += surface.Area

            case SurfaceType.Wall:
                self.__wallArea += surface.Area
                self.__windowArea += [x.Area for x in surface.Fenestrations]

        surface.Properties.ZoneName = self.Properties.Name
        self.__surfaces += [surface]

    def AddSurfaces(self, surfaces: list()):
        for surface in surfaces:
            if surface.Properties.ZoneName == self.Properties.Name: self.AddSurface(surface)