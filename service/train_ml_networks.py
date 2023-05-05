from service import logger, os, np, pd, shutil, tmp_dir
from MLModels.ml_models import get_regressor, get_generator

def train_regressor(info, probabilistic_parameters, sampled_parameters: np.ndarray, target_values: np.ndarray):
    logger.info(f'{info}Training Regressor')
    
    col = ["num_neurons", "reg_coeff", "learning_rate",]
    num_neurons1 = [20, 50, 100, 200]
    num_neurons2 = [0, 5, 10, 20]
    reg_coeff = [1e-3, 1e-4, 1e-5,]
    learnig_rate = [1e-2, 3e-3, 1e-3,]

    num_neurons = [[nn1, nn2] for nn1 in num_neurons1 for nn2 in num_neurons2]
    hyperparameters = pd.DataFrame([[n, r, l,] 
                                        for n in num_neurons
                                        for r in reg_coeff
                                        for l in learnig_rate
                                    ], columns = col).sample(n=2,)
    hyperparameters.reset_index(drop=True, inplace=True)

    network, loss = get_regressor(hyperparameters, sampled_parameters, target_values, probabilistic_parameters.GetScalingDF(),)
    
    logger.info(f'{info}Regressor Loss:\t{loss:.5f}')
    return network, loss

def train_generator(info, probabilistic_parameters, regressor, consumption):
    col = ["num_neurons", "reg_coeff", "learning_rate",]
    num_neurons1 = [20, 40, 60, 80, 100]
    num_neurons2 = [0, 5, 10, 15, 20, ]
    reg_coeff = [0,]
    learnig_rate = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4,]

    num_neurons = [[nn1, nn2] for nn1 in num_neurons1 for nn2 in num_neurons2]
    hyperparameters = pd.DataFrame([[n, r, l,] 
                                        for n in num_neurons
                                        for r in reg_coeff
                                        for l in learnig_rate
                                    ], columns = col).sample(n=60,)
    hyperparameters.reset_index(drop=True, inplace=True)

    targets = []
    for _ in range(100):
        targets += [list(np.random.choice(value) for _, value in consumption.iterrows())]
    targets = np.array(targets)

    logger.info(f'{info}training generator')
    for x in get_generator(hyperparameters, probabilistic_parameters.GetScalingDF(), regressor, targets, ):
        logger.info(f'{info}Generator Loss:\t{x[1]:.5f}')
        yield x