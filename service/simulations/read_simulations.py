"""Read EnergyPlus simulation output."""
import pandas as pd

from probabilistic.energy_predictions import EnergyPrediction
from probabilistic.energy_predictions import ProbabilisticEnergyPrediction


def read_simulations(
        num_samples: int,
        run_period_names: list,
        idf_folder: str):
    """Read EnergyPlus simulation output."""
    p_energies = []
    for i in range(num_samples):
        data = pd.read_csv(f'{idf_folder}/{i}.csv', index_col=0)
        data = data[[c for c in data.columns if 'Energy' in c]]
        data.index = run_period_names
        p_energies += [EnergyPrediction(None, data)]

    return ProbabilisticEnergyPrediction(None, p_energies).to_dict()
