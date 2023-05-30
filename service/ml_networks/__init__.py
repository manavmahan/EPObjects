import itertools
from service import pd

def sample_hyperparameters(hyperparameters_dict, sample_size):
    columns = hyperparameters_dict.keys()
    _, values = zip(*hyperparameters_dict.items())
    hp1 = list(itertools.product(*values))
    hps = pd.DataFrame(hp1, columns=columns)
    hps = hps.sample(min(len(hps), sample_size))
    hps.reset_index(drop=True, inplace=True)
    return hps