from ListObject import ListObject
from IDFObject.IDFObject import IDFObject
from IDFObject.ZoneVentilation.DesignFlowRate import DesignFlowRate

class ZoneList(IDFObject):
    __IDFName__ = 'ZoneList'
    Properties = [
        'Name',
        'ZoneNames',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        self.Initialise()

    def AddZone(self, zoneName):
        self.ZoneNames.Values += [zoneName]

    def Initialise(self):
        if isinstance(self.ZoneNames, str):
            self.ZoneNames = ListObject(self.ZoneNames.split(';'))

    def GetNaturalVentilationObject(self) -> DesignFlowRate:
        obj = DesignFlowRate(getattr(DesignFlowRate, "Default"))
        obj.Name = f"Natural Ventilation for {self.Name}"
        obj.ZoneListName = self.Name
        obj.ScheduleName = f"{self.Name}.People"
        return obj
