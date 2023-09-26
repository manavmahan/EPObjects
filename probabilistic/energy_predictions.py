"""Classes for storing EnergyPlus output."""
import numpy as np
import pandas as pd
import re

from EnumTypes import Frequency

CONVERTER = 2.77778e-10
ENERGIES = [
    # 'Lights Electric Energy',
    'Water to Air Heat Pump Electricity Energy',
    'Boiler Electricity Energy',
    'Cooling Tower Fan Electricity Energy',
]


class EnergyPrediction:
    """Holds energy predictions of EnergyPlus."""

    __frequency = Frequency.Annual

    @property
    def frequency(self):
        """Get the frequency of energy predictions."""
        return self.__frequency

    def __init__(self, name, data: pd.DataFrame = None, **kwargs):
        """Initialise energy prediction from EnergyPlus output."""
        self.Name = name
        self.Values = pd.DataFrame()
        if self.Name is not None:
            data_named = data[[c for c in data.columns
                               if re.findall(self.Name, c, re.IGNORECASE)]]
        else:
            data_named = data

        data_named *= CONVERTER
        for e in ENERGIES:
            values = data_named[[c for c in data.columns
                                 if re.findall(e, c, re.IGNORECASE)]]
            self.Values[e] = values.sum(axis=1)

        self.Values['Total'] = self.Values.sum(axis=1)

        if len(self.Values) == 12:
            self.__frequency = Frequency.Monthly
        if len(self.Values) == 8760:
            self.__frequency = Frequency.Hourly

    def __repr__(self):
        """Return string representation."""
        return f'{self.Name}\n{str(self.Values)}'


class ProbabilisticEnergyPrediction:
    """Used to store probabilistic energy predictions."""

    def __init__(self, name, energy) -> None:
        """Initialise from energy predictions (DataFrame)."""
        self.Name = name
        if isinstance(energy, dict):
            self.Values = energy
        else:
            self.Values = dict()
            if self.Name is None:
                energy_named = energy
            else:
                energy_named = list(e for e in energy if e.Name == self.Name)

            self.Values['Total'] = 0
            for e in ENERGIES:
                values = np.array((x.Values[e].values for x in energy_named))
                self.Values[e] = pd.DataFrame(
                    values,
                    columns=energy_named[0].Values.index)

                if 'Total' in self.Values:
                    self.Values['Total'] += self.Values[e]
                else:
                    self.Values['Total'] = self.Values[e]

    def to_dict(self):
        """Return dictionary representation."""
        return dict(
                    Name=self.Name,
                    Values=dict((x, self.Values[x].to_dict())
                                for x in self.Values)
                )

    @classmethod
    def from_json(cls, data):
        """Load object from JSON ."""
        values = dict((x, pd.DataFrame.from_dict(data['Values'][x]))
                      for x in data['Values'])
        return ProbabilisticEnergyPrediction(data["Name"], values)

    def get_mean(self):
        """Return mean of energy values."""
        for e in ENERGIES:
            yield {e: self.Values[e].mean(axis=0)}

    def get_summary(self):
        """Return summary of energy values."""
        for e in ENERGIES:
            yield {e: {
                'Mean': self.Values[e].mean(axis=0),
                'Min': self.Values[e].min(axis=0),
                'Max': self.Values[e].max(axis=0),
                'Total': self.Values[e].sum(axis=0),
            }}
