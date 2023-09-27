"""Tests for probabilistic module."""
import pandas as pd
import unittest

from probabilistic.parameter import Parameter, ProbabilisticParameter
from probabilistic.probabilistic_parameters import ProbabilisticParameters
from enum_types import SurfaceType, Distribution, ParameterType, SamplingScheme


class TestProbabilisticParameter(unittest.TestCase):
    """Tests for probabilistic parameter."""

    def setUp(self) -> None:
        """Set up at class instantiation."""
        parameter_1 = Parameter(f'{ParameterType.UValue}:{SurfaceType.Floor}')
        p_parameter_1 = ProbabilisticParameter(
            parameter_1, distribution=Distribution.Uniform, min=0.15, max=0.25)

        parameter_2 = Parameter(str(ParameterType.GValue), )
        p_parameter_2 = ProbabilisticParameter(
            parameter_2, distribution=Distribution.Normal,
            mean=0.8, standard_deviation=0.05)

        self.p_parameters = ProbabilisticParameters(
            [p_parameter_1, p_parameter_2])

    def test_uniform(self):
        """Test parameter with uniform distribution."""
        parameter = Parameter(
            f"{ParameterType.UValue}:{SurfaceType.Floor}")
        p_parameter = ProbabilisticParameter(
            parameter, distribution=Distribution.Uniform, min=0, max=10)
        self.assertEqual('u-value:Floor', str(p_parameter))
        self.assertEqual('u-value:Floor,5.0,5.0,Uniform',
                         p_parameter.as_csv())

    def test_lhs_sampling(self):
        """Test LHS sampling of parameter."""
        calculated_str = "u-value:Floor,0.2,0.05,Uniform\n" + \
            "g-value,0.8,0.05,Normal"
        self.assertEqual(calculated_str, self.p_parameters.as_csv())
        samples = self.p_parameters.generate_samples_as_df(
            3, sampling_scheme=SamplingScheme.LHS)
        calculated = {
            'u-value:Floor': {0: 0.1944, 1: 0.17976, 2: 0.24404},
            'g-value': {0: 0.77778, 1: 0.78294, 2: 0.8562},
        }
        self.assertDictEqual(samples.to_dict(), calculated)

    def test_mc_sampling(self):
        """Test random sampling of parameter."""
        samples = self.p_parameters.generate_samples_as_df(
            3, sampling_scheme=SamplingScheme.MonteCarlo)
        calculated = {
            'u-value:Floor': {0: 0.23929, 1: 0.23212, 2: 0.16077},
            'g-value': {0: 0.77828, 1: 0.71343, 2: 0.81203},
        }
        self.assertDictEqual(samples.to_dict(), calculated)


if __name__ == '__main__':
    unittest.main()
