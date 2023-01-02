from json import JSONEncoder, JSONDecoder
import numpy as np
import inspect
import sys

from GeometryObject.XYZ import XYZ
from GeometryObject.XYZList import XYZList

class IDFObject():
    def __init__(self, properties: list(), propertiesDict: dict()):
        for property in properties:
            if property in propertiesDict: setattr(self, property, propertiesDict[property])

    def ToDict(self):
        for key in self.Properties:
            yield key, getattr(self, key)

    @property
    def IDF(self) -> str:
        return f'''{self.__IDFName__},{','.join(str(getattr(self, x)).rstrip() for x in self.Properties)};'''

    def Initialise(self):
        '''
        Initialises IDFObject attribute from data.
        '''
        pass

    @staticmethod
    def GetChildrenTypes():
        print (__name__)
        clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        return clsmembers

class IDFJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (XYZList)): 
            return str(obj)

        if isinstance(obj, (IDFObject)): 
            return dict(obj.ToDict())

        if not isinstance(obj, str):
            return str(obj)

class IDFJsonDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct):
        for cls in IDFObject.__subclasses__():
            if list(dct.keys()) == cls.Properties:
                return cls(dct)
        return dct