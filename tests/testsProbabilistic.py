import unittest

from enum_types import SamplingScheme
from probabilistic.parameter import ProbabilisticParameters

class test1(unittest.TestCase):
    def testReadFile(self):
        pps = ProbabilisticParameters.ReadCsv("Probabilistic/1.csv")
        print (pps.AsCsv())
        print (pps.GenerateSamples(10))
        self.assertEqual(None, None)

    def testReadFile2(self):
        pps = ProbabilisticParameters.ReadCsv("Probabilistic/1.csv")
        print (pps.AsCsv())
        print (pps.GenerateSamples(10, SamplingScheme.MonteCarlo))
        self.assertEqual(None, None)

    def testReadFile3(self):
        pps = ProbabilisticParameters.ReadCsv("Probabilistic/1.csv")
        print (pps.AsCsv())
        print (pps.GenerateSamples(10, SamplingScheme.Sobol))
        self.assertEqual(None, None)

if __name__ == '__main__':
    unittest.main()