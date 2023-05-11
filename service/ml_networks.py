from service import logger, os, np, pd, shutil, tmp_dir
from MLModels.ml_models import get_regressor, get_generator, predict, get_scaling_parameters

def train_regressor(info, probabilistic_parameters, sampled_parameters: np.ndarray, target_values: np.ndarray, HYPERPARAMETERS: pd.DataFrame, NUMS: int, **kwargs):
    logger.info(f'{info}Training Regressor')
    
    hyperparameters = pd.DataFrame.from_dict(HYPERPARAMETERS).sample(n=NUMS,)
    hyperparameters.reset_index(drop=True, inplace=True)
    network, loss = get_regressor(hyperparameters, sampled_parameters, target_values, probabilistic_parameters.GetScalingDF(),)

    logger.info(f'{info}Regressor Loss:\t{loss:.5f}')
    return network, loss

def train_generator(info, probabilistic_parameters, regressor, consumption, HYPERPARAMETERS: pd.DataFrame, NUMS: int, **kwargs):
    hyperparameters = pd.DataFrame.from_dict(HYPERPARAMETERS).sample(n=NUMS,)
    hyperparameters.reset_index(drop=True, inplace=True)

    targets = []
    for _ in range(100):
        # targets += [list(np.random.choice(value) for _, value in consumption.iterrows())]
        # targets += [consumption[np.random.choice(consumption.columns)]]
        targets += [consumption.mean(axis=1)]
    targets = np.array(targets)
    
    logger.info(f'{info}training generator')
    for i, x in enumerate(get_generator(hyperparameters, probabilistic_parameters.GetScalingDF(), regressor, targets, )):
        logger.info(f'{info}Generator Loss {i}:\t{x[1]:.5f}')
        yield x

def predict_parameters(info, generator, regressor, num_samples_per_generator):
    parameters = predict(generator, None, num_samples_per_generator)
    results = predict(regressor, parameters,)
    return parameters, results