from service import logger, os, pd, shutil, tmp_dir
from MLModels.Regressor import get_regressor

def train_networks(user_name, project_name, probabilistic_parameters, sampled_parameters: pd.DataFrame, target_values):
    prepend_info = f'User: {user_name}\tProject: {project_name}\t'
    regressor, loss = train_regressor(probabilistic_parameters, sampled_parameters, target_values)

def train_regressor(probabilistic_parameters, sampled_parameters: pd.DataFrame, target_values):
    col = ["NN", "RC", "LR",]
    N1 = [20, 50, 100, 200]
    N2 = [0, 5, 10, 20]
    RC = [1e-3, 1e-4, 1e-5,]
    LR = [1e-2, 3e-3, 1e-3,]

    nn = [[nn1, nn2] for nn1 in N1 for nn2 in N2]
    hyperparameters = pd.DataFrame([[n, r, l,] 
                                        for n in nn
                                        for r in RC
                                        for l in LR
                                    ], columns = col).sample(n=60,)
    hyperparameters.index = range(len(hyperparameters))[:2]

    network, loss = get_regressor(hyperparameters, sampled_parameters, target_values, probabilistic_parameters.GetScalingDF(),)
    return network, loss

Logger.FinishTask('Training regressor')

Logger.StartTask('Training generator')
col = ["NN", "RC", "LR",]
N1 = [20, 40, 60, 80, 100]
N2 = [0, 5, 10, 15, 20, ]
RC = [0,]
LR = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4,]

nn = [[nn1, nn2] for nn1 in N1 for nn2 in N2]
hyperparameters = pd.DataFrame([[n, r, l,] 
                                    for n in nn
                                    for r in RC
                                    for l in LR
                                ], columns = col).sample(frac=1,)
hyperparameters.index = range(len(hyperparameters))

consumption = consumption.values.T
targetValues = consumption[[np.random.randint(0, len(consumption)) for _ in range(125)]]

revScalingDF_X = pps.GetScalingDFFromFile(f'{ProjectDirectory}/Parameters.csv')
m = GetGenerator(hyperparameters, 100, samples.columns, f'{MLFolder}/Generator', f'{r.FilePath}.h5', targetValues, revScalingDF=revScalingDF_X, training=simulate or trainRegressor or trainGenerator)

Logger.FinishTask('Training generator')
Logger.StartTask('Determining parameters')

dfs = m.Predict(10,)

# print (dfs.shape)
for p in dfs.columns:
    print (p, np.min(dfs[p]), np.percentile(dfs[p], 2.5), np.percentile(dfs[p], 50), dfs[p].mean(), np.percentile(dfs[p], 97.5), np.max(dfs[p]))

Logger.PrintSummary()