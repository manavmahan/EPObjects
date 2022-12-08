import pandas as pd

class IDFObject():
    def __init__(self, properties: list(), propertiesDict: dict()):
        for property in properties:
            if property in propertiesDict: setattr(self, property, propertiesDict[property])

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'''{self.__IDFName__},{','.join(str(getattr(self, x)).rstrip() for x in self.Properties)};'''

    def AsDict(self):
        return self.Properties

    def Initialise(self):
        '''
        Initialises IDFObject attribute from the data.
        '''
        pass

