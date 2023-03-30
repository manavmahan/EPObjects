from json import JSONEncoder, JSONDecoder
import inspect
import sys

from GeometryObject.XYZ import XYZ
from GeometryObject.XYZList import XYZList

class IDFObject():
    
    def __init__(self, properties: list(), propertiesDict: dict()):
        for property in properties:
            if property in propertiesDict: setattr(self, property, propertiesDict[property])

    def ToDict(self):
        for key in ["__IDFName__"] + self.Properties:
            yield key, getattr(self, key)

    @property
    def IDF(self) -> str:
        try: return f'''{self.__IDFName__},{','.join(str(getattr(self, x)).rstrip() for x in self.Properties)};'''
        except: raise Exception(self.__IDFName__)

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
            try:
                return dict(obj.ToDict())
            except:
                raise Exception(obj.__IDFName__)

        if not isinstance(obj, str):
            return str(obj)

class IDFJsonDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct):
        if "__IDFName__" in dct.keys():
            return IDFObject.SubclassesAndIDFName[dct["__IDFName__"]](dct)
        try:
            return IDFObject.SubclassesAndProperties[','.join(dct.keys())](dct)
        except KeyError:
            raise Exception(f"Cannot find subclass for {list(dct.keys())} from {IDFObject.SubclassesAndProperties}")