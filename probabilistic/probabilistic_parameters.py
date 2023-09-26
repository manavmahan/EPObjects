"""Probabilistic parameters for a list of probabilistic parameters."""

import math
import numpy as np
import pandas as pd

from enum_types import SamplingScheme

from probabilistic.helper import get_sampling_matrix
from probabilistic.parameter import ProbabilisticParameter


class ProbabilisticParameters:
    """Class to store a list of probabilistic parameters."""

    def __init__(self, parameters: list()):
        """Initialise probabilistic parameters."""
        self.__index = 0
        self.__parameters = parameters

    def __iter__(self):
        """Iterate through parameters."""
        self.current = self.__parameters[0]
        self.__index = 0
        return self

    def __next__(self):
        """Get next parameter."""
        try:
            self.__index += 1
            return self.__parameters[self.__index - 1]
        except IndexError:
            raise StopIteration

    def as_csv(self):
        """Return parameters in csv format."""
        return '\n'.join(x.as_csv() for x in self.__parameters)

    def generate_samples(
            self,
            num: int,
            scheme=SamplingScheme.LHS):
        """Generate samples."""
        self.__sampling_scheme = scheme
        matrix = get_sampling_matrix(
            self.__sampling_scheme,
            num, len(self.__parameters))
        result = np.empty(matrix.shape)
        for i, p in enumerate(self.__parameters):
            result[:, i] = p.get_scaled_parameters(matrix[:, i])
        return result

    def generate_samples_as_df(
            self,
            num_samples: int,
            sampling_scheme=SamplingScheme.LHS):
        """Create samples as a pd.DataFrame."""
        samples = self.generate_samples(num_samples, sampling_scheme)
        return pd.DataFrame(samples,
                            columns=(str(x) for x in self.__parameters))

    def get_scaling_df(self):
        """Create a pd.DataFrame to min-max scaling."""
        df = pd.DataFrame(columns=['Min', 'Range'])
        for _, pp in enumerate(self.__parameters):
            df.loc[str(pp.Parameter)] = pp.get_scaling_df().values
        return df

    def get_scaling_df_from_file(self, file):
        """Create a pd.DataFrame to min-max scaling."""
        ra = pd.read_csv(file, index_col=0)
        df = pd.DataFrame(columns=['Min', 'Range'])
        for _, pp in enumerate(self.__parameters):
            name = str(pp.Parameter)
            df.loc[name] = pp.GetScalingDF().values

            if math.isnan(ra.loc[name, 'Low']):
                low = 0
            else:
                low = ra.loc[name, 'Low']

            if math.isnan(ra.loc[name, 'High']):
                high = 1
            else:
                high = ra.loc[name, 'High']

            df.loc[name, 'Min'] += df.loc[name, 'Range'] * low
            df.loc[name, 'Range'] *= (high-low)
        return df

    @classmethod
    def from_df(cls, df,):
        """Generate probabilistic parameters from a pd.DataFrame."""
        pps = []
        for _, x in df.iterrows():
            if not x.name.startswith('#'):
                pp = ProbabilisticParameter.read_csv(x.name, *x.values)
                pps += [pp]
        return ProbabilisticParameters(pps)

    @classmethod
    def read_csv(cls, file,):
        """Generate probabilistic parameters from a file."""
        df = pd.read_csv(file, index_col=0)
        return cls.from_df(df)
