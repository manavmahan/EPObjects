import importlib

import os

import pandas as pd

from EnumTypes import ParameterType, SurfaceType
from ListObject import ListObject

from IDFObject.Building import Building
from IDFObject.BuildingSurface.Detailed import Detailed
from IDFObject.Zone import Zone

from Probabilistic import Parameter

class IDFFile:
    Properties = [
        "Building",
        "BuildingSurface_Detailed",
        "Construction",
        "ConvergenceLimits",
        "Daylighting_Controls",
        "Daylighting_ReferencePoint",
        "ElectricEquipment",
        "HVACTemplate_Plant_Boiler",
        "HVACTemplate_Plant_MixedWaterLoop",
        "HVACTemplate_Plant_Tower",
        "HVACTemplate_Thermostat",
        "HVACTemplate_Zone_WaterToAirHeatPump",
        "InternalMass",
        "Lights",
        "Material",
        "Output_Diagnostics",
        "Output_PreprocessorMessage",
        "Output_Surfaces_Drawing",
        "Output_Table_SummaryReports",
        "Output_Variable",
        "Output_VariableDictionary",
        "OutputControl_Table_Style",
        "People",
        "RunPeriod",
        "Schedule_Compact",
        "ScheduleTypeLimits",
        "SimulationControl",
        "Site_GroundTemperature_BuildingSurface",
        "Site_Location",
        "SizingPeriod_WeatherFileDays",
        "Timestep",
        "Version",
        "WindowMaterial_Shade",
        "WindowMaterial_SimpleGlazingSystem",
        "WindowShadingControl",
        "Zone",
        "ZoneInfiltration_DesignFlowRate",
        "ZoneList"
    ]

    ProbablisticParameters = list()

    def __init__(self, directory=None, baseDirectory='Data'):
        for p in self.Properties:
            className = ['IDFObject'] + p.split('_')
            module = importlib.import_module('.'.join(className))
            fileName = f'{directory}/{":".join(className[1:])}.txt'
            if not os.path.isfile(fileName):
                fileName = f'{baseDirectory}/{":".join(className[1:])}.txt'
                if not os.path.isfile(fileName):
                    print (fileName)
                    continue
            
            class_ = getattr(module, className[-1])
            data = pd.read_csv(fileName)
            epObjects = []
            for name in data.index:
                epObjects += [class_(data.loc[name].to_dict())]
            setattr(self, p, epObjects)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = ""
        for x in self.Properties:
            for obj in getattr(self, x):
                string += str(obj) + '\n'
        return string

    def QueryParameter (self, parameterType: ParameterType, surfaceType: SurfaceType, zone: str = None, name: str = None) -> Parameter:
        exception = Exception(f"Cannot find {parameterType} for {surfaceType} with {zone} and {name} from {self.__probablisticParameters}.")

        matches = list(x for x in self.__probablisticParameters if x.Parameter.Type == parameterType and x.Element == str(surfaceType))
        if zone: matches = list(x for x in self.__probablisticParameters if x.Zone == zone)
        if name: matches = list(x for x in self.__probablisticParameters if x.Name == name)
        
        if len(matches) == 0:
            raise exception