import numpy as np
import pandas as pd
import re

from EnumTypes import Frequency

Converter = 2.77778e-10
Energies = [
    'Lights Electric Energy',
    'Water to Air Heat Pump Electric Energy',
    'Boiler Electric Energy',
    'Cooling Tower Fan Electric Energy',
]

class EnergyPrediction:
    __frequency = Frequency.Annual
    @property
    def Frequencey(self):
        return self.__frequency
        
    def __init__(self, name, data: pd.DataFrame=None, **kwargs):
        self.Name = name
        self.Values = pd.DataFrame()
        dataNamed = data[[c for c in data.columns if re.findall(self.Name, c, re.IGNORECASE)]] if self.Name is not None else data
        dataNamed = dataNamed * Converter
        for e in Energies:
            self.Values[e] = dataNamed[[c for c in data.columns if re.findall(e, c, re.IGNORECASE)]].sum(axis=1)

        self.Values['Total'] = self.Values.sum(axis=1)

        if len(self.Values) == 12: self.__frequency = Frequency.Monthly
        if len(self.Values) == 8760: self.__frequency = Frequency.Hourly

    def __repr__(self):
        return f'{self.Name}\n{str(self.Values)}'

class ProbabilisticEnergyPrediction:
    def __init__(self, name, energy: list()) -> None:
        self.Name = name
        self.Values = dict()

        energyNamed = energy if self.Name is None else list(en for en in energy if en.Name == self.Name)
        for e in Energies:
            self.Values[e] = pd.DataFrame(np.array(list(x.Values[e].values for x in energyNamed)), columns=energyNamed[0].Values.index)
            if 'Total' in self.Values:
                self.Values['Total'] = self.Values['Total'] + self.Values[e]
            else:
                self.Values['Total'] = self.Values[e]

    def GetMean(self):
        for e in Energies:
            yield {e: self.Values[e].mean(axis=0)}

    def GetSummary(self):
        for e in Energies:
            yield {e: {
                'Mean': self.Values[e].mean(axis=0),
                'Min': self.Values[e].min(axis=0),
                'Max': self.Values[e].max(axis=0),
                'Total': self.Values[e].sum(axis=0),
            }}