import numpy as np
import os
import pandas as pd
import shutil

from sklearn.model_selection import KFold, train_test_split

from tensorflow.keras.activations import relu, sigmoid, hard_sigmoid

from tensorflow.keras.callbacks import EarlyStopping

from tensorflow.keras.layers import Activation, Dense, InputLayer, Rescaling

from tensorflow.keras.models import load_model

from tensorflow.keras.losses import mean_squared_error, MeanSquaredError
MSE = MeanSquaredError()

from tensorflow.keras.optimizers import Adam

from tensorflow.keras.regularizers import L2, Regularizer

from tensorflow.keras import Sequential

from tensorflow import _logging
_logging.disable(_logging.DEBUG)
_logging.disable(_logging.INFO)
_logging.disable(_logging.WARNING)

import time

EarlyStoppingLoss = EarlyStopping(monitor='loss', min_delta=1e-05, patience=20, restore_best_weights=True,)
EarlyStoppingValLoss = EarlyStopping(monitor='val_loss', min_delta=1e-05, patience=20, restore_best_weights=True,)

def GetScalingLayer(dataset=None, scaledDF=None, reverse=False, allColumnsEqual=False):
    if scaledDF is None: scaledDF = GetScalingParameters(dataset, allColumnsEqual)
    if reverse:
        return Rescaling(scaledDF['Range'].values, offset = scaledDF['Min'].values)
    else:
        return Rescaling(1./scaledDF['Range'].values, offset = (-scaledDF['Min']/scaledDF['Range']).values)

def GetScalingParameters(dataDF, allColumnsEqual):
    df = pd.DataFrame(index = dataDF.columns)
    df['Min'] = dataDF.values.min() * np.ones(len(dataDF.columns)) if allColumnsEqual else dataDF.min(axis=0) 
    df['Max'] = dataDF.values.max() * np.ones(len(dataDF.columns)) if allColumnsEqual else dataDF.max(axis=0)
    df['Range'] = df['Max'] - df['Min']
    return df

class Regressor():
    def __init__(self, features, targets, filePath):
        self.Features = features
        self.Targets = targets
        self.NumFeatures = len(self.Features)
        self.NumTargets = len(self.Targets)
        self.FilePath = filePath

    def __getModel(self, hyperparameters, scalingX, revScalingY=None):
        model = Sequential()
        model.add(InputLayer(input_shape = (self.NumFeatures, )))
        model.add(scalingX)
       
        for nn in (n for n in hyperparameters['NN'] if n>0):
            model.add( Dense(nn, activation=relu, kernel_regularizer=L2(hyperparameters['RC'])) )

        model.add(Dense(self.NumTargets))
        if revScalingY is not None: model.add(revScalingY)
        
        model.compile(loss=mean_squared_error, optimizer=Adam(learning_rate=hyperparameters['LR']),)
        return model

    def __trainModel(self, hyperparameters, XTrain, YTrain, XVal, YVal, scalingX, revScalingY=None):
        model = self.__getModel(hyperparameters, scalingX, revScalingY)
        if XVal is None:
            history = model.fit(XTrain, YTrain, epochs=1000, verbose=0, callbacks=[EarlyStoppingLoss],)
            return model, MSE(YTrain, model(XTrain, training=False).numpy()).numpy()
        else:
            history = model.fit(XTrain, YTrain, validation_data=[XVal, YVal], epochs=1000, verbose=0, callbacks=[EarlyStoppingValLoss],)
            return model, min(history.history['val_loss']) 

    def GetBestHyperparameters(self, hyperparametersSet, X, Y, scalingDF_X, numFolds=5):
        print (f'Searching best hyperparameters using {numFolds} folds cross validation...')
        if os.path.exists(self.FilePath): shutil.rmtree(self.FilePath)
        os.makedirs(self.FilePath)

        kfold = KFold(n_splits=numFolds, shuffle=True)
        
        scalingX = GetScalingLayer(X, scalingDF_X)
        scalingY = GetScalingLayer(Y, allColumnsEqual=False, reverse=True)

        bestLoss = float('inf')
        bestHP = None
        for i, hp in hyperparametersSet.iterrows():
            print (f'Hyperparameters:\t{dict(hp)}')
            loss = []
            f=0
            for train, val in kfold.split(X, Y):
                print (f'Fold No.:\t{f}')
                model, foldLoss = self.__trainModel(hp, X.values[train], Y.values[train], X.values[val], Y.values[val], scalingX, scalingY)
                loss += [foldLoss]
                f += 1
            loss = np.array(loss).mean()
            print (f'Cross-validation loss:\t{loss}')
            if loss < bestLoss:
                bestLoss = loss
                bestHP = hp

        return bestHP, bestLoss, scalingX, scalingY

    def TuneHyperparameters(self, hyperparametersSet, X, Y, scalingDF_X=None):
        scalingX = GetScalingLayer(X, scalingDF_X)
        scalingY = GetScalingLayer(Y, allColumnsEqual=False, reverse=True)

        modelLoss = float('inf')
        for i, hp in hyperparametersSet.iterrows():
            X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=0)
            m, loss = self.__trainModel(hp, X, Y, X_val, Y_val, scalingX, scalingY)
            print (f'MSE:\t{loss};\tMean (Y):\n{Y.mean()}')
            if loss < modelLoss:
                modelLoss = loss
                m.save(f"{self.FilePath}.h5")

    def Predict(self, data,):
        model = load_model(f"{self.FilePath}.h5")
        predictedY = model.predict(data[self.Features], verbose=0)
        data[[f"Predicted_{x}" for x in self.Targets]] = predictedY
        return data