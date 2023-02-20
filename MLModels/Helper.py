from MLModels.Regressor import Regressor
from MLModels.Generator import Generator

def TrainRegressor(hyperparameters, X, Y, filePath, scalingDF_X=None, training=False):
    m = Regressor(X.columns, Y.columns, filePath)
    if training: m.TuneHyperparameters(hyperparameters, X, Y, scalingDF_X)
    return m

def TrainGenerator(hyperparameters, numInputs, parameters, filePath, regressorFilePath, targetValues, revScaling, training=False):
    m = Generator(numInputs, parameters, filePath)
    if training: m.TuneHyperparameters(hyperparameters, regressorFilePath, targetValues, revScaling)
    return m