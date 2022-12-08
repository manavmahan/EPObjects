import numpy as np

from ListObject import ListObject
from IDFObject.IDFObject import IDFObject
from IDFObject.Material import Material
from IDFObject.WindowMaterial import SimpleGlazingSystem

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
        uvalue = sum(m.Thickness/m.Conductivity for m in self.Materials)
        return np.round(uvalue, 5)

    def __init__(self, properties: dict(), materials: list()=None) -> None:
        super().__init__(self.Properties, properties)
        self.MaterialsName = ListObject(self.MaterialsName.split(';'))
        self.Materials = list()
        if materials is not None:
            self.Initialise(materials)

    def __updateMaterialNames(self):
        self.MaterialsName = ListObject([x.Name for x in self.Materials])

    def Initialise(self, materials: list()):
        for mName in self.MaterialsName.Values:
            material = next(x for x in materials if x.Name==mName)
            if material is None:
                raise Exception(f"Material {mName} is not found.")
            self.Materials += [next(x for x in materials if x.Name==mName)]

    def AdjustGValue(self, requiredGValue):
        if self.GValue != requiredGValue:
            self.Materials[0].GValue = requiredGValue
            self.Materials[0].Name = self.Materials[0].Name + "." + self.Name
            self.__updateMaterialNames()

    def AdjustUValue(self, requiredUValue, insulation: str):
        if (self.UValue == requiredUValue):
            return
        
        if (isinstance(self.Materials[0], SimpleGlazingSystem)):
            self.Material[0].UValue = requiredUValue
            self.__updateMaterialNames()

        uWithoutInsulation = sum(m.Thickness/m.Conductivity for m in self.Materials if m.Name != insulation)
        insulationThickness = np.round(insulation.Conductivity * ((1/requiredUValue) - uWithoutInsulation), 5)
        if insulationThickness < 0:
            raise Exception(f"Cannot have insulation layer of less than zero thickness. u-value: {requiredUValue}.")
        
        insulationLayer = next(x for x in self.Materials if x.Name == insulation)
        if insulationThickness == 0:
            del insulationLayer
        else:
            insulationLayer.Properties.Thickness = insulationThickness
            insulationLayer.Name = insulationLayer.Name + "." + self.Name
        
        self.__updateMaterialNames()

Construction.ExternalWall = dict(
    Name = 'ExternalWall',
    MaterialsName = 'Plaster;Insulation;Brick*Wall;Plaster'
)

Construction.FloorCeiling = dict(
    Name = 'FloorCeiling',
    MaterialsName = 'Concrete*Floor;Insulation;Screed*Floor'
)

Construction.GroundFloor = dict(
    Name = 'GroundFloor',
    MaterialsName = 'PerimeterInsulation;Insulation;Concrete*Floor;Screed*Floor'
)

Construction.InternalWall = dict(
    Name = 'InternalWall',
    MaterialsName = 'PlasterBoard;Insulation;PlasterBoard'
)

Construction.Roof = dict(
    Name = 'Roof',
    MaterialsName = 'PerimeterInsulation;Insulation;Concrete*Roof;Plaster'
)

Construction.Glazing = dict(
    Name = 'Glazing',
    MaterialsName = 'Glazing'
)