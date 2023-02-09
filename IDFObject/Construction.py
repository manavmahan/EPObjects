import copy

import numpy as np

from ListObject import ListObject

from IDFObject.IDFObject import IDFObject

from IDFObject.Material import Material

from IDFObject.WindowMaterial.SimpleGlazingSystem import SimpleGlazingSystem

class Construction(IDFObject):
    __IDFName__ = "Construction"
    Properties = [
        'Name',
        'MaterialsName',
    ]

    @property
    def GValue(self):
        gValue = self.Materials[0].GValue
        return np.round(gValue, 5)

    @property
    def UValue(self):
        if all(isinstance(x, Material) for x in self.Materials):
            uvalue = 1/sum(m.Thickness/m.Conductivity for m in self.Materials)
        elif all(isinstance(x, SimpleGlazingSystem) for x in self.Materials):
            uvalue = sum(m.UFactor for m in self.Materials)
        else:
            raise NotImplementedError("Compound construction!")
        return np.round(uvalue, 5)

    def __init__(self, properties: dict(), materials: list()=None) -> None:
        super().__init__(self.Properties, properties)
        self.MaterialsName = ListObject(self.MaterialsName.split(';'))
        self.Materials = list()
        self.Initialise(materials)

    def __updateMaterialNames(self):
        self.MaterialsName = ListObject([x.Name for x in self.Materials])

    def Initialise(self, materials: list()):
        if materials is None:
            return
        for mName in self.MaterialsName.Values:
            self.Materials += [next(x for x in materials if x.Name==mName)]

    def AdjustGValue(self, requiredGValue):
        if self.Materials[0].SolarHeatGainCoefficient != requiredGValue:
            self.Materials[0].SolarHeatGainCoefficient = requiredGValue

    def AdjustUValue(self, requiredUValue, insulation: str="Insulation"):
        if not requiredUValue: return
        if (self.UValue == requiredUValue):
            return
        
        if (isinstance(self.Materials[0], SimpleGlazingSystem)):
            self.Materials[0].UFactor = requiredUValue
            return

        insulationLayer = next(x for x in self.Materials if x.Name == insulation)
        
        resistanceWithoutInsulation = sum(m.Thickness/m.Conductivity for m in self.Materials if m.Name != insulation)
        insulationThickness = np.round(insulationLayer.Conductivity * ((1/requiredUValue) - resistanceWithoutInsulation), 5)
        if insulationThickness < 0:
            raise Exception(f"Cannot have insulation layer of less than zero thickness. u-value: {requiredUValue}.")
        
        if insulationThickness == 0:
            del insulationLayer
        else:
            insulationLayerMod = copy.deepcopy(insulationLayer)
            insulationLayerMod.Thickness = insulationThickness
            insulationLayerMod.Name = insulationLayer.Name + "." + self.Name

        self.Materials[self.Materials.index(insulationLayer)] = insulationLayerMod
        self.__updateMaterialNames()
        return insulationLayerMod

Construction.ExternalWall = dict(
    Name = 'ExternalWall',
    MaterialsName = 'Plaster;Insulation;Brick.Wall;Plaster'
)

Construction.FloorCeiling = dict(
    Name = 'FloorCeiling',
    MaterialsName = 'Concrete.Floor;Insulation;Screed.Floor'
)

Construction.Glazing = dict(
    Name = 'Glazing',
    MaterialsName = 'Glazing'
)

Construction.GroundFloor = dict(
    Name = 'GroundFloor',
    MaterialsName = 'PerimeterInsulation;Insulation;Concrete.Floor;Screed.Floor'
)

Construction.InternalWall = dict(
    Name = 'InternalWall',
    MaterialsName = 'PlasterBoard;Insulation;PlasterBoard'
)

Construction.Mass = dict(
    Name = 'Mass',
    MaterialsName = "Mass",
)

Construction.Roof = dict(
    Name = 'Roof',
    MaterialsName = 'PerimeterInsulation;Insulation;Concrete.Roof;Plaster'
)