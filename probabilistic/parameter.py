import math
import numpy as np
import pandas as pd

from SALib.sample import sobol_sequence as sobol

from scipy.stats.distributions import norm, uniform, triang

from enum_types import Distribution, ParameterType, SamplingScheme

def GetLHSMatrix(numSamples, numParameters) -> np.ndarray:
    rs=np.random.RandomState(seed=numSamples * numParameters)
    result = np.empty([numSamples, numParameters])
    d = 1.0 / numSamples
    for i in range(numParameters):
        s = np.empty([numSamples])
        for j in range(numSamples):
            s[j] = rs.uniform(low=j * d, high=(j + 1) * d)
        rs.shuffle(s)
        result[:, i] = s
    return result

def GetMonteCarloMatrix(numSamples, numParameters) -> np.ndarray:
    rs = np.random.RandomState(seed=numSamples * numParameters)
    return rs.rand(numSamples, numParameters)

def GetSobolMatrix(numSamples, numParameters) -> np.ndarray:
    return sobol.sample(numSamples, numParameters)

def GetSamplingMatrix(samplingScheme: SamplingScheme, numSamples: int, numParameters: int,) -> np.ndarray:
    if samplingScheme == SamplingScheme.LHS:
        return GetLHSMatrix(numSamples, numParameters)
    elif samplingScheme == SamplingScheme.MonteCarlo:
        return GetMonteCarloMatrix(numSamples, numParameters)
    elif samplingScheme == SamplingScheme.Sobol:
        return GetSobolMatrix(numSamples, numParameters)

class Parameter:
    '''Initialise a parameter by its type and name.
    Check @ParameterType for possible parameter types.
    kwargs may contain key:
        ZoneList: for creating properties at zone list level.
        Zone: for creating properties for instance of a zone.
        Element: for creating properties for a type of element such as wall, floor, etc.
        Instance: for the most detailed level at instance of any element type.
    '''
    Splitter = ':'

    def __init__(self, args) -> None:
        self.Type = ParameterType(args.split(Parameter.Splitter)[0])
        self.Name = args

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.Name

class ProbabilisticParameter:
    def __init__(self, parameter: Parameter, distribution: Distribution=Distribution.Uniform, min=None, max=None, mean=None, variation=None, standardDeviation=None):
        self.Distribution = distribution
        if self.Distribution==Distribution.Uniform or self.Distribution==Distribution.Triangular:
            if max:
                if min is None:
                    raise Exception("Invalid probabilistic parameter: minimum and maximum value should be provided.")
                self.Min = min
                self.Max = max
                self.Mean = 0.5 * (self.Max + self.Min)
                self.Variation = 0.5 * (self.Max - self.Min)

            if mean:
                if variation is None:
                    raise Exception("Invalid probabilistic parameter: mean and variation value should be provided.")
                self.Mean = mean
                self.Variation = variation
                self.Min = self.Mean - self.Variation
                self.Max = self.Mean + self.Variation
            
        elif self.Distribution == Distribution.Normal:
                if standardDeviation is None:
                    raise Exception("Invalid probabilistic parameter: mean and standardDeviation value should be provided.")
                self.Mean = mean
                self.StandardDeviation = standardDeviation
                self.Min = self.Mean - 3*self.StandardDeviation
                self.Max = self.Mean + 3*self.StandardDeviation

        self.Parameter = parameter

    def __str__(self) -> str:
        return str(self.Parameter)

    def __repr__(self) -> str:
        return self.__str__()

    def AsCsv(self):
        return ','.join([
            self.__str__(), 
            str(self.Mean), 
            str(self.Variation if self.Distribution != Distribution.Normal else self.StandardDeviation),
            str(self.Distribution),
        ])

    def AsDict(self):
        value = dict(
            Name = self.__str__(),
            Mean = self.Mean,
            Distribution = self.Distribution,
        )
        if self.Distribution == Distribution.Uniform or self.Distribution == Distribution.Triangular:
            value["Variation"] = self.Variation
        else:
            value["StandardDeviation"] = self.StandardDeviation
        return value

    def GetScalingDF(self):
        return pd.Series([self.Min, self.Max-self.Min], name=str(self.Parameter))

    def GetScaledParameters(self, samplingArray):
        if self.Distribution == Distribution.Normal:
            result = norm(loc=self.Mean, scale=self.StandardDeviation).ppf(samplingArray)
        elif self.Distribution == Distribution.Triangular:
            result = triang(loc=self.Mean, scale=self.Variation, c=0.5).ppf(samplingArray)
        elif self.Distribution == Distribution.Uniform:
            result = self.Min + 2 * self.Variation * samplingArray
        return np.round(result, 5)

    @staticmethod
    def ReadCsv(*values):
        parameter = Parameter(values[0])
        distribution = Distribution(values[3])

        if distribution == Distribution.Uniform or distribution == Distribution.Triangular:
            return ProbabilisticParameter(parameter, distribution=distribution, mean=float(values[1]), variation=float(values[2]))
        else:
            return ProbabilisticParameter(parameter, distribution=distribution, mean=float(values[1]), standardDeviation=float(values[2]))

class ProbabilisticParameters:
    def __init__(self, parameters: list()):
        self.__index = 0
        self.__parameters = parameters

    def __iter__(self):
        self.current = self.__parameters[0]
        self.__index = 0
        return self

    def __next__(self):
        try:
            self.__index += 1
            return self.__parameters[self.__index - 1]
        except IndexError:
            raise StopIteration

    def AsCsv(self):
        return '\n'.join(x.AsCsv() for x in self.__parameters)

    def GenerateSamples(self, numSamples : int, samplingScheme=SamplingScheme.LHS):
        self.__samplingScheme = samplingScheme
        samplingMatrix = GetSamplingMatrix(self.__samplingScheme, numSamples, len(self.__parameters))
        result = np.empty(samplingMatrix.shape)
        for i, p in enumerate(self.__parameters):
            result[:, i] = p.GetScaledParameters(samplingMatrix[:, i])
        return result

    def GenerateSamplesAsDF(self, numSamples : int, samplingScheme=SamplingScheme.LHS):
        return pd.DataFrame(self.GenerateSamples(numSamples, samplingScheme), columns=(str(x) for x in self.__parameters))

    def get_names(self):
        return list([str(x.Parameter) for x in self.__parameters])

    def get_scaling_df(self):
        df = pd.DataFrame(columns=['Min', 'Range'])
        for _, pp in enumerate(self.__parameters):
            df.loc[str(pp.Parameter)] = pp.GetScalingDF().values
        return df

    def GetScalingDFFromFile(self, file):
        ra = pd.read_csv(file, index_col=0)
        df = pd.DataFrame(columns=['Min', 'Range'])
        for _, pp in enumerate(self.__parameters):
            df.loc[str(pp.Parameter)] = pp.GetScalingDF().values
        
            low = 0 if math.isnan(ra.loc[str(pp.Parameter), 'Low']) else ra.loc[str(pp.Parameter), 'Low']
            high = 1 if math.isnan(ra.loc[str(pp.Parameter), 'High']) else ra.loc[str(pp.Parameter), 'High']
            
            df.loc[str(pp.Parameter), 'Min'] += df.loc[str(pp.Parameter), 'Range'] * low
            df.loc[str(pp.Parameter), 'Range'] *= (high-low)

        return df
    
    @classmethod
    def from_df(cls, parameters,):
        return ProbabilisticParameters([ProbabilisticParameter.ReadCsv(x.name, *x.values) for _, x in parameters.iterrows()if not x.name.startswith('#')] )

    @classmethod
    def read_csv(cls, file,):
        parameters = pd.read_csv(file, index_col=0)
        return ProbabilisticParameters([ProbabilisticParameter.ReadCsv(x.name, *x.values) for _, x in parameters.iterrows()if not x.name.startswith('#')] )