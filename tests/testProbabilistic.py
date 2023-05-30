import pandas as pd
import unittest

from probabilistic.parameter import Distribution, Parameter, ParameterType, ProbabilisticParameter, ProbabilisticParameters, SamplingScheme
from enum_types import SurfaceType

class TestParameter(unittest.TestCase):
    def testFloor(self):
        parameter = Parameter(ParameterType.UValue, Element=str(SurfaceType.Floor),)
        self.assertEqual('u-value*Floor', str(parameter))

    def testWallWithAllFeatures(self):
        parameter = Parameter(ParameterType.UValue, Element=str(SurfaceType.Wall), Zone="Zone-1", Name="Floor-1 in Zone-1")
        self.assertEqual('u-value*Wall*Zone-1*Floor-1 in Zone-1', str(parameter))

class TestProbabilisticParameter(unittest.TestCase):
    def testUniform(self):
        parameter = Parameter(ParameterType.UValue, Element=str(SurfaceType.Floor),)
        pParameter = ProbabilisticParameter(parameter, distribution=Distribution.Uniform, min=0, max=10)
        self.assertEqual('u-value*Floor', str(pParameter))
        self.assertEqual('u-value*Floor,5.0,10,Uniform', pParameter.WriteToCsv())

    Parameter1 = Parameter(ParameterType.UValue, Element=str(SurfaceType.Floor), )
    PParameter1 = ProbabilisticParameter(Parameter1, distribution=Distribution.Uniform, min=0.15, max=0.25)

    Parameter2 = Parameter(ParameterType.GValue, )
    PParameter2 = ProbabilisticParameter(Parameter2, distribution=Distribution.Normal, mean=0.8, standardDeviation=0.05)

    PParameters = ProbabilisticParameters([PParameter1, PParameter2])
        
    def testSampling(self):
        self.assertEqual('u-value*Floor,0.2,0.1,Uniform\ng-value,0.8,0.05,Normal', self.PParameters.WriteToCsv())

        samples = self.PParameters.GenerateSamplesAsDF(3, samplingScheme=SamplingScheme.LHS)
        samplesCalc = { 
                        'u-value*Floor': {0: 0.1944, 1: 0.17976, 2: 0.24404}, 
                        'g-value': {0: 0.77778, 1: 0.78294, 2: 0.8562},
                    }
        self.assertDictEqual(samples.to_dict(), samplesCalc)

    def testMCSampling(self):
        samples = self.PParameters.GenerateSamplesAsDF(3, samplingScheme=SamplingScheme.MonteCarlo)
        samplesCalc = { 
                        'u-value*Floor': {0: 0.23929, 1: 0.23212, 2: 0.16077}, 
                        'g-value': {0: 0.77828, 1: 0.71343, 2: 0.81203},
                    }
        self.assertDictEqual(samples.to_dict(), samplesCalc)
if __name__ == '__main__':
    unittest.main()
