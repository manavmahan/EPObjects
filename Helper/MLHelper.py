from MLModels.Regressor import Regressor, GetScalingLayer, Rescaling
from MLModels.Generator import Generator

def GetRegressor(hyperparameters, features, targets, filePath, X, Y, scalingDF_X=None, training=False):
    m = Regressor(features, targets, filePath)
    if training: m.TuneHyperparameters(hyperparameters, X, Y, scalingDF_X)
    return m

def GetGenerator(hyperparameters, numInputs, parameters, filePath, regressorFilePath, targetValues, revScalingDF, training=False):
    m = Generator(numInputs, parameters, filePath)
    if training: m.TuneHyperparameters(hyperparameters, regressorFilePath, targetValues, revScalingDF)
    return m