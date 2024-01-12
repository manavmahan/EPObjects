"""Helper methods for ML networks."""
import itertools
from service.helper import pd


def sample_hyperparameters(hyperparameters_dict, sample_size=None):
    """Create combinations hyperparameters."""
    columns = hyperparameters_dict.keys()
    num_neurons = hyperparameters_dict.get('num_neurons')
    hyperparameters_dict['num_neurons'] = list(itertools.product(*num_neurons))

    _, values = zip(*hyperparameters_dict.items())
    hp1 = list(itertools.product(*values))
    hps = pd.DataFrame(hp1, columns=columns)
    
    df_size = len(hps)
    if sample_size is None or sample_size>df_size :
        sample_size = df_size
    hps = hps.sample(sample_size)
    hps.reset_index(drop=True, inplace=True)
    return hps
