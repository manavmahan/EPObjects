import copy

import numpy as np

from string_list import StringList

from idf_object import IDFObject
from idf_object.material import Material
from idf_object.material.air_gap import AirGap
from idf_object.windowmaterial.simpleglazingsystem import SimpleGlazingSystem

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
        uvalue = 1./ Construction.get_resistance(self.Materials)
        return np.round(uvalue, 5)
    
    default = dict()
    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.MaterialsName = StringList(self.MaterialsName)

    def __updateMaterialNames(self):
        self.MaterialsName = StringList([x.Name for x in self.Materials])

    def initialise_materials(self, materials: list()):
        self.Materials = list()
        for mName in self.MaterialsName:
            try: self.Materials += [next(x for x in materials if x.Name==mName)]
            except StopIteration: raise KeyError(f'material {mName} not found for {self.Name}.')

    @staticmethod
    def get_resistance(materials):
        if all(isinstance(x, Material) for x in materials):
            r = sum(m.Thickness/m.Conductivity for m in materials)
        elif all(isinstance(x, SimpleGlazingSystem) for x in materials):
            r = sum(m.UFactor for m in materials)
        elif all(isinstance(x, (Material, AirGap)) for x in materials):
            materials = list(x for x in materials if isinstance(x, Material))
            air_gaps = list(x for x in materials if isinstance(x, AirGap))
            r =  sum([m.Thickness/m.Conductivity for m in materials])
            r += sum([m.Resistance for m in air_gaps])
        else:
            raise NotImplementedError("Compound construction!")
        return r

    def AdjustUGValue(self, requiredUValue, requiredGValue):
        if self.Materials[0].SolarHeatGainCoefficient != requiredGValue or self.Materials[0].UFactor != requiredUValue:
            self.Materials[0] = copy.deepcopy(self.Materials[0])
            self.Materials[0].Name = self.Materials[0].Name + "." + self.Name
            if self.Materials[0].SolarHeatGainCoefficient != requiredGValue:
                self.Materials[0].SolarHeatGainCoefficient = requiredGValue

            if  self.Materials[0].UFactor != requiredUValue:
                self.Materials[0].UFactor = requiredUValue
            self.__updateMaterialNames()
            return self.Materials[0]
        return None

    def adjust_properties(self, require_uvalue: float = None, requiredGValue: float = None, insulation: str="Insulation"):
        if not require_uvalue and not requiredGValue: return
        if (self.UValue == require_uvalue):
            return
        
        if (isinstance(self.Materials[0], SimpleGlazingSystem)):
            return self.AdjustUGValue(require_uvalue, requiredGValue)

        try:
            insulation_layer = next(x for x in self.Materials if x.Name == insulation)
        except StopIteration:
            insulation_layer = next(x for x in self.Materials if insulation in x.Name)
        
        resistance_without_insulation = Construction.get_resistance(list(m for m in self.Materials if m.Name != insulation_layer.Name))
        insulation_thickness = np.round(insulation_layer.Conductivity * ((1/require_uvalue) - resistance_without_insulation), 5)
        if insulation_thickness < 0:
            raise Exception(f"Cannot have insulation layer {insulation_layer.Name} of thickness {insulation_thickness}. u-value: {require_uvalue}, R-value (without insulation layer): {resistance_without_insulation}. Materials: {', '.join([x.Name for x in self.Materials])}")
        
        if insulation_thickness == 0:
            del insulation_layer
        else:
            new_insulation_layer = copy.deepcopy(insulation_layer)
            new_insulation_layer.Thickness = insulation_thickness
            new_insulation_layer.Name = insulation_layer.Name + "." + self.Name

        self.Materials[self.Materials.index(insulation_layer)] = new_insulation_layer
        self.__updateMaterialNames()
        return new_insulation_layer

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