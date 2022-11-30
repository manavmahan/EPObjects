import numpy as np
import pandas as pd

from SALib.sample import sobol_sequence as sobol

from scipy.stats.distributions import norm, uniform, triang

from EnumTypes import Distribution, ParameterType, SamplingScheme

@staticmethod
def GetLHSMatrix(numSamples, numParameters) -> np.ndarray:
    print (numSamples, numParameters)
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

@staticmethod
def GetMonteCarloMatrix(numSamples, numParameters) -> np.ndarray:
    rs = np.random.RandomState(seed=numSamples * numParameters)
    return rs.rand(numSamples, numParameters)

@staticmethod
def GetSobolMatrix(numSamples, numParameters) -> np.ndarray:
    return sobol.sample(numSamples, numParameters)

@staticmethod
def GetSamplingMatrix(samplingScheme: SamplingScheme, numSamples: int, numParameters: int,) -> np.ndarray:
    match samplingScheme:
        case SamplingScheme.LHS:
            return GetLHSMatrix(numSamples, numParameters)
        case SamplingScheme.MonteCarlo:
            return GetMonteCarloMatrix(numSamples, numParameters)
        case SamplingScheme.Sobol:
            return GetSobolMatrix(numSamples, numParameters)

class Parameter:
    Type : ParameterType = None
    Unit : str = ''
    Value: float = None

    # Identification Properties
    Element : str = None            # Examples: Floor, Roof, Light Heat Gain
    Name : str = None               # Examples: Floor-0 in Zone-1
    Zone : str = None               # Examples: Zone-0

    __delimeter = '*'

    def __init__(self, type, **kwargs) -> None:
        self.Type = type
        if (kwargs.__contains__('Zone')):
            self.Zone = kwargs['Zone']
        if (kwargs.__contains__('Element')):
            self.Element = kwargs['Element']
        if (kwargs.__contains__('Name')):
            self.Name = kwargs['Name']

    def __str__(self) -> str:
        return self.__delimeter.join([x for x in [str(self.Type), self.Element, self.Zone, self.Name] if x])

class ProbabilisticParameter:
    Max = 0.0
    Mean = 0.0
    Min = 0.0
    
    Variation = 0.0
    StandardDeviation = 0.0

    Distribution : Distribution = Distribution.Uniform
    Parameter : Parameter = None

    Values = None

    def __init__(self, parameter: Parameter, distribution: Distribution=Distribution.Uniform, min=None, max=None, mean=None, variation=None, standardDeviation=None):
        self.Distribution = distribution
        match self.Distribution:
            case Distribution.Uniform | Distribution.Triangular:
                if max:
                    if min is None:
                        raise Exception("Invalid probabilistic parameter: minimum and maximum value should be provided.")
                    self.Min = min
                    self.Max = max
                    self.Mean = 0.5 * (self.Max + self.Min)
                    self.Variation = self.Max - self.Min

                if mean:
                    if not variation:
                        raise Exception("Invalid probabilistic parameter: mean and variation value should be provided.")
                    self.Mean = mean
                    self.Variation = variation
                    self.Min = self.Mean - 0.5 * self.Variation
                    self.Max = self.Mean + 0.5 * self.Variation
            
            case Distribution.Normal:
                if not standardDeviation:
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

    def AsDict(self):
        value = dict(Name = self.__str__())
        value["Mean"] = self.Mean
        if self.Distribution == Distribution.Uniform or self.Distribution == Distribution.Triangular:
            value["Variation"] = self.Variation
            value["Distribution"] = self.Distribution
        else:
            value["StandardDeviation"] = self.StandardDeviation
            value["Distribution"] = self.Distribution
        return value

    def GetScaledParameters(self, samplingArray):
        match self.Distribution:
            case Distribution.Normal:
                result = norm(loc=self.Mean, scale=self.StandardDeviation).ppf(samplingArray)
            case Distribution.Triangular:
                result = triang(loc=self.Mean, scale=self.StandardDeviation, c=0.5).ppf(samplingArray)
            case Distribution.Uniform:
                result = self.Min + (self.Max - self.Min) * samplingArray
        return np.round(result, 5)

    def WriteToCsv(self):
        return ','.join(str(x) for x in self.AsDict().values())

class ProbabilisticParameters:
    __samplingScheme = SamplingScheme.LHS

    def __init__(self, parameters: list()):
        self.__index = 0
        self.__parameters = parameters

    def __iter__(self):
        self.current = self.__parameters[0]
        return self

    def __next__(self):
        try:
            self.__index += 1
            return self.__parameters[self.__index - 1]
        except IndexError:
            raise StopIteration

    def GenerateSamples(self, numSamples : int, samplingScheme=SamplingScheme.LHS):
        self.__samplingScheme = samplingScheme
        samplingMatrix = GetSamplingMatrix(self.__samplingScheme, numSamples, len(self.__parameters))
        result = np.empty(samplingMatrix.shape)
        for i, p in enumerate(self.__parameters):
            result[:, i] = p.GetScaledParameters(samplingMatrix[:, i])
        return result

    def GenerateSamplesAsDF(self, numSamples : int, samplingScheme=SamplingScheme.LHS):
        return pd.DataFrame(self.GenerateSamples(numSamples, samplingScheme), columns=(str(x) for x in self.__parameters))

    def WriteToCsv(self):
        return '\n'.join(x.WriteToCsv() for x in self.__parameters)