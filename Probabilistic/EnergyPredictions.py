import numpy as np
import pandas as pd
import re

from ..EnumTypes import Frequency

class EnergyPredictionZone:
    Name: str = None
    Loads = {
        'Heating Load': None,
        'Cooling Load': None,
        'Lights Load': None,
    }

    __frequency = Frequency.Annual
    @property
    def Frequencey(self):
        return self.__frequency
        
    def __init__(self, name, data: pd.DataFrame=None, loads: dict()=None, frequency: Frequency = None, **kwargs):
        if data is None and loads is None:
            raise Exception("Cannot intialise empty object.")

        self.Name = name
        if loads is None:
            for load in self.Loads.keys():
                self.Loads[load] = data[next(c for c in data.combine if re.match(f'^{self.Name}*{load}*'))]
        else:
            for load in self.Loads.keys():
                if load in loads: self.Loads[load] = loads[load]

        if not frequency and len(self.HeatingLoad) > 1:
            match len(self.Loads['Heating Load']):
                case 12:
                    self.__frequency = Frequency.Monthly
            self.__frequency = Frequency.Hourly

class ProbabilisticEnergyPredictionZone:
    Name: str = None
    Loads = {
        'Heating Load': None,
        'Cooling Load': None,
        'Lights Load': None,
    }
    EnergyPredictionZone: list()
    
    def __init__(self, energyPredictions: list()) -> None:
        self.EnergyPredictionZone = energyPredictions 
        for load in self.Loads.keys():
            self.Loads[load] = np.array((x[load] for x in self.EnergyPredictionZone))

    def GetMean(self):
        for l in self.EnergyPredictionZone[0].Loads:
            yield {l: self.Loads[l].mean()}

    def GetSummary(self):
        for l in self.Loads:
            yield {l: {
                'Mean': self.Loads[l].mean(),
                'Min': self.Loads[l].min(),
                'Max': self.Loads[l].max(),
            }}