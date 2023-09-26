"""Module for helper functions."""
import numpy as np
from SALib.sample import sobol_sequence as sobol

from enum_types import SamplingScheme


def get_lhs_matrix(num_samples, num_parameters) -> np.ndarray:
    """Create LHS matrix."""
    rs = np.random.RandomState(seed=num_samples * num_parameters)
    result = np.empty([num_samples, num_parameters])
    d = 1.0 / num_samples
    for i in range(num_parameters):
        s = np.empty([num_samples])
        for j in range(num_samples):
            s[j] = rs.uniform(low=j * d, high=(j + 1) * d)
        rs.shuffle(s)
        result[:, i] = s
    return result


def get_monte_carlo_matrix(num_samples, num_parameters) -> np.ndarray:
    """Create random matrix."""
    rs = np.random.RandomState(seed=num_samples * num_parameters)
    return rs.rand(num_samples, num_parameters)


def get_sobol_matrix(num_samples, num_parameters) -> np.ndarray:
    """Create sobol matrix."""
    return sobol.sample(num_samples, num_parameters)


def get_sampling_matrix(
        sampling_scheme: SamplingScheme,
        num_samples: int,
        num_parameters: int,) -> np.ndarray:
    """Create sample matrix."""
    if sampling_scheme == SamplingScheme.LHS:
        return get_lhs_matrix(num_samples, num_parameters)
    elif sampling_scheme == SamplingScheme.MonteCarlo:
        return get_monte_carlo_matrix(num_samples, num_parameters)
    elif sampling_scheme == SamplingScheme.Sobol:
        return get_sobol_matrix(num_samples, num_parameters)
