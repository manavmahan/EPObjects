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
    
    default = dict()
    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        
        if isinstance(self.MaterialsName, str):
            self.MaterialsName = ListObject(self.MaterialsName.split(','))
        self.Materials = list()

    def __updateMaterialNames(self):
        self.MaterialsName = ListObject([x.Name for x in self.Materials])

    def initialise_materials(self, materials: list()):
        for mName in self.MaterialsName.Values:
            try: self.Materials += [next(x for x in materials if x.Name==mName)]
            except StopIteration: raise StopIteration(f'material {mName} not found.')

    def AdjustUGValue(self, requiredUValue, requiredGValue):
        if self.Materials[0].SolarHeatGainCoefficient != requiredGValue or self.Materials[0].UFactor != requiredUValue:
            self.Materials[0] = copy.deepcopy(self.Materials[0])
            self.Materials[0].Name = self.Materials[0].Name + "." + self.Name
            if self.Materials[0].SolarHeatGainCoefficient != requiredGValue:
                self.Materials[0].SolarHeatGainCoefficient = requiredGValue

            if  self.Materials[0].UFactor != requiredUValue:
                self.Materials[0].UFactor = requiredGValue
            self.__updateMaterialNames()
            return self.Materials[0]
        return None

    def AdjustProperties(self, requiredUValue: float = None, requiredGValue: float = None, insulation: str="Insulation"):
        if not requiredUValue and not requiredGValue: return
        if (self.UValue == requiredUValue):
            return
        
        if (isinstance(self.Materials[0], SimpleGlazingSystem)):
            return self.AdjustUGValue(requiredUValue, requiredGValue)

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

    @staticmethod
    def initialise_material_layers(ep_objects):
        materials = list(x for x in ep_objects if isinstance(x, (Material, SimpleGlazingSystem)))
        for construction in [x for x in ep_objects if isinstance(x, Construction)]:
            for mName in construction.MaterialsName.Values:
                construction.Materials += [next(x for x in materials if x.Name==mName)]

    WallExternal = dict(
        Name = 'WallExternal',
        MaterialsName = 'Plaster,Insulation,Brick.Wall,Plaster'
    )

    FloorInternal = dict(
        Name = 'FloorInternal',
        MaterialsName = 'Concrete.Floor,Insulation,Screed.Floor'
    )

    Glazing = dict(
        Name = 'Glazing',
        MaterialsName = 'Glazing'
    )

    FloorGround = dict(
        Name = 'FloorGround',
        MaterialsName = 'PerimeterInsulation,Insulation,Concrete.Floor,Screed.Floor'
    )

    WallInternal = dict(
        Name = 'WallInternal',
        MaterialsName = 'PlasterBoard,Insulation,PlasterBoard'
    )

    Mass = dict(
        Name = 'Mass',
        MaterialsName = "Mass",
    )

    Roof = dict(
        Name = 'Roof',
        MaterialsName = 'PerimeterInsulation,Insulation,Concrete.Roof,Plaster'
    )

    Window = dict(
        Name = 'Window',
        MaterialsName = 'Window'
    )