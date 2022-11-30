
from EnumTypes import ParameterType, SurfaceType

from IDFObjects.Building import Building
from IDFObjects.BuildingSurface.Detailed import Surface
from IDFObjects.Zone import Zone

from Probabilistic import Parameter

class IDFFile:
    # included in IDF File
    Building = Building
    Zones = list()

    ProbablisticParameters = list()

    def QueryParameter (self, parameterType: ParameterType, surfaceType: SurfaceType, zone: str = None, name: str = None) -> Parameter:
        exception = Exception(f"Cannot find {parameterType} for {surfaceType} with {zone} and {name} from {self.__probablisticParameters}.")

        matches = list(x for x in self.__probablisticParameters if x.Parameter.Type == parameterType and x.Element == str(surfaceType))
        if zone: matches = list(x for x in self.__probablisticParameters if x.Zone == zone)
        if name: matches = list(x for x in self.__probablisticParameters if x.Name == name)
        
        if len(matches) == 0:
            raise exception


    def IDFString(self):
        return f'''
            {self.Building}\n
            {(str(x) for x in self.Zone)}\n
        '''
