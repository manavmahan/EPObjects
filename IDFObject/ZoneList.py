from ListObject import ListObject
from IDFObject.IDFObject import IDFObject

from IDFObject.ElectricEquipment import ElectricEquipment

from IDFObject.Lights import Lights

from IDFObject.People import People

from IDFObject.HVACTemplate.Thermostat import Thermostat

from IDFObject.ZoneInfiltration.DesignFlowRate import DesignFlowRate as Infiltration

from IDFObject.ZoneVentilation.DesignFlowRate import DesignFlowRate as Ventilation

class ZoneList(IDFObject):
    __IDFName__ = 'ZoneList'
    Properties = [
        'Name',
        'ZoneNames',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.Initialise()

    def AddZone(self, zoneName):
        self.ZoneNames.Values += [zoneName]

    def Initialise(self):
        if isinstance(self.ZoneNames, str):
            self.ZoneNames = ListObject(self.ZoneNames.split(';'))

    def GetDefaultVentilationObject(self, minimal=False) -> Ventilation:
        ventilation = dict(Ventilation.Minimal if minimal else Ventilation.Default) 
        ventilation.update(dict(
            Name = f"Default Ventilation for {self.Name}",
            ZoneListName = self.Name,
            ScheduleName = 'Generic.Always1' if minimal else f"{self.Name}.People",
        ))
        return Ventilation(ventilation)

    def GetInfiltrationObject(self, ach=0.3) -> Infiltration:
        infiltration = dict(Infiltration.Default)
        infiltration.update(dict(
                Name = f"Infiltration for {self.Name}",
                ZoneListName = self.Name,
                ScheduleName = f"Generic.Always1",
                AirChangesperHour = ach,
            )
        )
        return Infiltration(infiltration)

    def GetNaturalVentilationObject(self) -> Ventilation:
        ventilation = dict(Ventilation.Natural)
        ventilation.update(dict(
            Name = f"Natural Ventilation for {self.Name}",
            ZoneListName = self.Name,
            ScheduleName = f"{self.Name}.People"
        ))
        return Ventilation(ventilation)

    def GetElectricEquipmentObject(self, wpm) -> ElectricEquipment:
        ee = dict(ElectricEquipment.Default)
        ee.update(
            dict(
                Name = f"ElectricEquipment.{self.Name}",
                ZoneListName = self.Name,
                ScheduleName = f"{self.Name}.ElectricEquipment",
                WattsperZoneFloorArea = wpm,
            )
        )
        return ElectricEquipment(ee)

    def GetLightsObject(self, wpm) -> Lights:
        lights = dict(Lights.Default)
        lights.update(
            dict(
                Name = f"Lights.{self.Name}",
                ZoneListName = self.Name,
                ScheduleName = f"{self.Name}.Lights",
                WattsperZoneFloorArea = wpm,
            )
        )
        return Lights(lights)

    def GetPeopleObject(self, occupancy) -> People:
        people = dict(People.Default)
        people.update(
            dict(
                Name = f"People.{self.Name}",
                ZoneListName = self.Name,
                NumberofPeopleScheduleName = f"{self.Name}.People",
                ActivityLevelScheduleName = f"{self.Name}.Activity",
                ZoneFloorAreaperPerson = occupancy,
            )
        )
        return People(people)

    def GetThermostatObject(self, fixedSetPoints=None) -> Thermostat:
        t = Thermostat(Thermostat.Default)
        t.Name = f"Thermostat.{self.Name}"

        if fixedSetPoints:
            t.ConstantHeatingSetpoint = fixedSetPoints[0]
            t.ConstantCoolingSetpoint = fixedSetPoints[1]
        else:
            t.HeatingSetpointScheduleName = f"{self.Name}.HeatingSetpoint"
            t.CoolingSetpointScheduleName = f"{self.Name}.CoolingSetpoint"
        return t