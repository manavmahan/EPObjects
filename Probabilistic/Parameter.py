import numpy as np
import pandas as pd

from SALib.sample import sobol_sequence as sobol

from scipy.stats.distributions import norm, uniform, triang

from EnumTypes import Distribution, ParameterType, SamplingScheme

@staticmethod
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
    '''Initialise a parameter by its type and name.
    Check @ParameterType for possible parameter types.
    kwargs may contain key:
        ZoneList: for creating properties at zone list level.
        Zone: for creating properties for instance of a zone.
        Element: for creating properties for a type of element such as wall, floor, etc.
        Instance: for the most detailed level at instance of any element type.
    '''
    def __init__(self, type, **kwargs) -> None:
        self.Type = ParameterType(type)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.Type},{self.ZoneList},{self.Zone},{self.Element},{self.Instance}"

    @staticmethod
    def ReadCsv(args):
        return Parameter(args[0], ZoneList = args[1], Zone = args[2], Element = args[3], Instance = args[4],)

class ProbabilisticParameter:
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
                    self.Variation = 0.5 * (self.Max - self.Min)

                if mean:
                    if not variation:
                        raise Exception("Invalid probabilistic parameter: mean and variation value should be provided.")
                    self.Mean = mean
                    self.Variation = variation
                    self.Min = self.Mean - self.Variation
                    self.Max = self.Mean + self.Variation
            
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

    def GetScaledParameters(self, samplingArray):
        match self.Distribution:
            case Distribution.Normal:
                result = norm(loc=self.Mean, scale=self.StandardDeviation).ppf(samplingArray)
            case Distribution.Triangular:
                result = triang(loc=self.Mean, scale=self.Variation, c=0.5).ppf(samplingArray)
            case Distribution.Uniform:
                result = self.Min + (2.0 * self.Variation) * samplingArray
        return np.round(result, 5)

    @staticmethod
    def ReadCsv(line):
        values = line.split(',')
        print (values)
        parameter = Parameter.ReadCsv(values[:5])
        mean = float(values[5])
        
        distribution = Distribution(values[7])

        if distribution == Distribution.Uniform or distribution == Distribution.Triangular:
            return ProbabilisticParameter(parameter, distribution=distribution, mean=mean, variation=float(values[6]))
        else:
            return ProbabilisticParameter(parameter, distribution=distribution, mean=mean, standardDeviation=float(values[6]))

class ProbabilisticParameters:
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

    @staticmethod
    def ReadCsv(file=None, parameters=None):
        if file is not None:
            with open(file) as f:
                parameters = f.readlines()
        return ProbabilisticParameters( [ProbabilisticParameter.ReadCsv(x.replace('\n', '')) for x in parameters] )