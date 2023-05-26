from StringList import StringList
from IDFObject.IDFObject import IDFObject

from IDFObject.ElectricEquipment import ElectricEquipment

from IDFObject.Lights import Lights

from IDFObject.People import People

from IDFObject.HVACTemplate.Thermostat import Thermostat

from IDFObject.ZoneInfiltration.DesignFlowRate import DesignFlowRate as Infiltration

from IDFObject.ZoneVentilation.DesignFlowRate import DesignFlowRate as Ventilation

class Zonelist(IDFObject):
    __IDFName__ = 'ZoneList'
    Properties = [
        'Name',
        'ZoneNames',
    ]

    default = dict()
    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.ZoneNames = StringList(self.ZoneNames.split(','))

    def get_default_ventilation(self, minimal=False) -> Ventilation:
        return Ventilation(
            default = 'minimal' if minimal else 'default', 
            Name = f"Default Ventilation for {self.Name}",
            ZoneListName = self.Name,
            ScheduleName = 'Generic.Always1' if minimal else f"{self.Name}.People",
        )

    def get_natutal_ventilation(self) -> Ventilation:
        return Ventilation(
            default = "Natural",
            Name = f"Natural Ventilation for {self.Name}",
            ZoneListName = self.Name,
            ScheduleName = f"{self.Name}.People"
        )

    def get_electric_equipment(self, wpm) -> ElectricEquipment:
        return ElectricEquipment(
            Name = f"ElectricEquipment.{self.Name}",
            ZoneListName = self.Name,
            ScheduleName = f"{self.Name}.ElectricEquipment",
            WattsperZoneFloorArea = wpm,
        )

    def get_lights(self, wpm) -> Lights:
        return Lights(
            Name = f"Lights.{self.Name}",
            ZoneListName = self.Name,
            ScheduleName = f"{self.Name}.Lights",
            WattsperZoneFloorArea = wpm,
        )

    def get_people(self, occupancy) -> People:
        return People(
            Name = f"People.{self.Name}",
            ZoneListName = self.Name,
            NumberofPeopleScheduleName = f"{self.Name}.People",
            ActivityLevelScheduleName = f"{self.Name}.Activity",
            ZoneFloorAreaperPerson = occupancy,
        )

    def get_thermostat(self, fixedSetPoints=None) -> Thermostat:
        t = Thermostat(Name = f"Thermostat.{self.Name}")

        if fixedSetPoints:
            t.ConstantHeatingSetpoint = fixedSetPoints[0]
            t.ConstantCoolingSetpoint = fixedSetPoints[1]
        else:
            t.HeatingSetpointScheduleName = f"{self.Name}.HeatingSP"
            t.CoolingSetpointScheduleName = f"{self.Name}.CoolingSP"
        return t