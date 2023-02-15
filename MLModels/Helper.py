from MLModels.MLModel import Regressor
from MLModels.Generator import Generator

def TrainRegressor(hyperparameters, X, Y, filePath):
    m = Regressor(X.columns, Y.columns, filePath)
    m.TuneHyperparameters(hyperparameters, X, Y)
    return m

def TrainGenerator(hyperparameters, numInputs, parameters, filePath, regressorFilePath, targetValues, revScaling):
    m = Generator(numInputs, parameters, filePath)
    m.TuneHyperparameters(hyperparameters, regressorFilePath, targetValues, revScaling)
    return m