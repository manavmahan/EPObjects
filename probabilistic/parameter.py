"""Parameter and probabilistic parameter module."""

import numpy as np
import pandas as pd
from scipy.stats.distributions import norm, triang

from EnumTypes import Distribution, ParameterType

INVALID_SD = Exception("Invalid probabilistic parameter. \
                       Provide mean and standard deviation.")

INVALID_VARIATION = Exception("Invalid probabilistic parameter. \
                              Provide mean and variation value.")

INVALID_MIN_MAX = Exception("Invalid probabilistic parameter. \
                            Provide minimum and maximum value.")


class Parameter:
    """Initialise a parameter by its type and name.

    Check @ParameterType for possible parameter types.
    kwargs may contain key:
        ZoneList: for creating properties at zone list level.
        Zone: for creating properties for instance of a zone.
        Element: for creating properties for a type of element such as wall.
        Instance: for the most detailed level at instance of any element type.
    """

    Splitter = ':'

    def __init__(self, args) -> None:
        """Initialise parameter."""
        self.Type = ParameterType(args.split(Parameter.Splitter)[0])
        self.Name = args

    def __repr__(self) -> str:
        """Create string representation."""
        return self.__str__()

    def __str__(self) -> str:
        """Create string representation."""
        return self.Name


class ProbabilisticParameter:
    """Probabilistic parameter class."""

    def __init__(self,
                 parameter: Parameter,
                 distribution: Distribution = Distribution.Uniform,
                 min=None, max=None, mean=None,
                 variation=None, standard_deviation=None):
        """Initialise probabilistic parameter."""
        self.Distribution = distribution
        if any(self.Distribution == Distribution.Uniform,
                self.Distribution == Distribution.Triangular):
            if max:
                if min is None:
                    raise INVALID_MIN_MAX
                self.Min = min
                self.Max = max
                self.Mean = 0.5 * (self.Max + self.Min)
                self.Variation = 0.5 * (self.Max - self.Min)

            if mean:
                if variation is None:
                    raise INVALID_VARIATION
                self.Mean = mean
                self.Variation = variation
                self.Min = self.Mean - self.Variation
                self.Max = self.Mean + self.Variation

        elif self.Distribution == Distribution.Normal:
            if standard_deviation is None:
                raise INVALID_SD
            self.Mean = mean
            self.StandardDeviation = standard_deviation
            self.Min = self.Mean - 3*self.StandardDeviation
            self.Max = self.Mean + 3*self.StandardDeviation

        self.Parameter = parameter

    def __str__(self) -> str:
        """Create string representation."""
        return str(self.Parameter)

    def __repr__(self) -> str:
        """Create string representation."""
        return self.__str__()

    def as_csv(self):
        """Create CSV representation."""
        if self.Distribution != Distribution.Normal:
            var_sd = self.Variation
        else:
            var_sd = self.StandardDeviation
        return ','.join([
            self.__str__(),
            str(self.Mean),
            str(var_sd),
            str(self.Distribution),
        ])

    def as_dict(self):
        """Create dictionary for a probabilistic parameter."""
        value = dict(
            Name=str(self),
            Mean=self.Mean,
            Distribution=self.Distribution,
        )

        uniform_trian = (Distribution.Uniform, Distribution.Triangular)
        if self.Distribution in uniform_trian:
            value["Variation"] = self.Variation
        else:
            value["StandardDeviation"] = self.StandardDeviation
        return value

    def get_scaling_df(self):
        """Create a line for scaling DF."""
        return pd.Series([self.Min, self.Max-self.Min],
                         name=str(self.Parameter))

    def get_scaled_parameters(self, sampling_array):
        """Get scaled value."""
        if self.Distribution == Distribution.Normal:
            result = norm(loc=self.Mean,
                          scale=self.StandardDeviation).ppf(sampling_array)
        elif self.Distribution == Distribution.Triangular:
            result = triang(loc=self.Mean,
                            scale=self.Variation, c=0.5).ppf(sampling_array)
        elif self.Distribution == Distribution.Uniform:
            result = self.Min + 2 * self.Variation * sampling_array
        return np.round(result, 5)

    @staticmethod
    def read_csv(*values):
        """Create a parameter from a csv line."""
        parameter = Parameter(values[0])
        d = Distribution(values[3])

        if d == Distribution.Uniform or d == Distribution.Triangular:
            return ProbabilisticParameter(
                parameter,
                distribution=d,
                mean=float(values[1]),
                variation=float(values[2])
            )
        else:
            return ProbabilisticParameter(
                parameter,
                distribution=d,
                mean=float(values[1]),
                standard_deviation=float(values[2])
            )
