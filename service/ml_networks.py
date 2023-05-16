from service import logger, os, np, pd, shutil, tmp_dir
import itertools
from service import db_functions as db
from MLModels.ml_models import get_regressor, get_generator, predict, get_scaling_parameters

def sample_hyperparameters(hyperparameters_dict, sample_size):
    columns = hyperparameters_dict.keys()
    _, values = zip(*hyperparameters_dict.items())
    hp1 = list(itertools.product(*values))
    hps = pd.DataFrame(hp1, columns=columns)
    hps = hps.sample(min(len(hps), sample_size))
    hps.reset_index(drop=True, inplace=True)
    return hps


def train_regressor(info, probabilistic_parameters, sampled_parameters: np.ndarray, target_values: np.ndarray, hyperparameters: dict, NUMS: int, **kwargs):
    logger.info(f'{info}Training Regressor')
    hyperparameters = sample_hyperparameters(hyperparameters, NUMS,)
    network, loss = get_regressor(hyperparameters, sampled_parameters, target_values, probabilistic_parameters.GetScalingDF(),)
    logger.info(f'{info}Regressor Loss:\t{loss:.5f}')
    return network, loss

def train_generator(info, probabilistic_parameters, regressor, consumption, hyperparameters: dict, NUMS: int, **kwargs):
    hyperparameters = sample_hyperparameters(hyperparameters, NUMS,)
    logger.info(f'{info}training generator')
    if kwargs.get(db.METHOD) == db.GENERATIVE:
        targets = np.array([consumption.mean(axis=1) for _ in range(125)])
        for i, x in enumerate(get_generator(hyperparameters, probabilistic_parameters.GetScalingDF(), regressor, targets, )):
            logger.info(f'{info}Generator Loss {i}:\t{x[1]:.5f}')
            yield x

def predict_parameters(info, generator, regressor, num_samples_per_generator):
    parameters = predict(generator, None, num_samples_per_generator)
    results = predict(regressor, parameters,)
    return parameters, results