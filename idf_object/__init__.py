import re
from json import JSONEncoder, JSONDecoder
from geometry_object.xyzlist import XYZList

class IDFObject():
    def __init__(self, properties: list(), propertiesDict: dict()):
        for property in properties:
            setattr(self, property, propertiesDict.get(property))

    def __eq__(self, other):
        if self.__IDFName__ != other.__IDFName__: 
            return False
        try: 
            return self.Name == other.Name
        except AttributeError: 
            return self.IDF == other.IDF

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

def custom_import(name):
    components = name.split(':')
    components.insert(0, 'idf_object')
    try:
        mod = __import__('.'.join(components).lower(), fromlist=[components[-1]])
    except ModuleNotFoundError:
        module = [re.sub(r'(?<!^)(?=[A-Z])', '_', x).lower() for x in components]
        mod = __import__('.'.join(module), fromlist=[module])
    return getattr(mod, components[-1])

class IDFJsonDecoder(JSONDecoder):
    SubclassesAndIDFName = dict()
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct):
        try:
            if "__IDFName__" in dct.keys():
                class_ = self.SubclassesAndIDFName.get(dct["__IDFName__"])
                if class_ is None:
                    try:
                        class_ = custom_import(dct["__IDFName__"])
                        self.SubclassesAndIDFName[dct["__IDFName__"]] = class_
                    except:
                        raise TypeError(f"{dct['__IDFName__']}")
                return self.SubclassesAndIDFName[dct["__IDFName__"]](**dct)
            else:
                raise TypeError("Old version object without __IDFName__")
        except TypeError:
            raise TypeError(f"{dct['__IDFName__']}")