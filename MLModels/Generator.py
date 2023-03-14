from functools import reduce
import glob
import numpy as np
import os
import pandas as pd
import shutil

from MLModels.Regressor import Activation, Adam, Dense, EarlyStoppingValLoss, L2, Sequential, InputLayer, mean_squared_error, MSE, Regularizer, Rescaling, relu, load_model, sigmoid, hard_sigmoid, time, GetScalingLayer

from tensorflow.random import normal
from tensorflow.keras import Model
from tensorflow.keras import backend as K

from tensorflow.keras.losses import Loss

from tensorflow import reduce_min

from tensorflow.math import square

from tensorflow.keras.utils import get_custom_objects
from tensorflow.keras.utils import register_keras_serializable
from tensorflow.math import add, log, abs, multiply, subtract, reduce_mean

@register_keras_serializable(package='Custom', name='CustomRegularizerHardSigmoid')
class CustomRegularizerHardSigmoid(Regularizer):
    def __init__(self, l2=1):
        self.l2 = l2

    def __call__(self, x):
        x = log(abs(multiply(x, 0.4)))
        x = add(x, abs(x))
        return reduce_mean(multiply(x, self.l2))

    def get_config(self):
        return {'l2': float(self.l2)}

class CustomLossMinimum(Loss):
    def call(self, y_true, y_pred):
        return reduce_min(square(y_pred - y_true), axis=-1)

class Generator():
    def __init__(self, numInputs, parameters, filePath):
        self.NumInputs = numInputs
        self.NumOutputs = len(parameters)
        self.Parameters = parameters
        self.FilePath = filePath

    def Input(self, numExamples):
        return np.random.random((numExamples, self.NumInputs)) * 100

    def __getModel(self, hyperparameters, appendModel, revScalingX):
        model = Sequential()
        model.add(InputLayer(input_shape = (self.NumInputs, )))

        for nn in [n for n in hyperparameters['NN'] if n>0]:
            model.add( Dense(nn, kernel_regularizer=L2(hyperparameters['RC']), activation=sigmoid,))

        model.add(Dense(self.NumOutputs, activity_regularizer=CustomRegularizerHardSigmoid()))
        model.add(Activation(hard_sigmoid))
        model.add(revScalingX)

        self.Generator = model
        outputs = appendModel(self.Generator.output)
        self.Model = Model(inputs=self.Generator.inputs, outputs=outputs)
        self.Model.compile(loss=CustomLossMinimum(), optimizer=Adam(learning_rate=hyperparameters['LR']))

    def __trainModel(self, hyperparameters, appendModelPath, actual, revScalingX):
        appendModel = load_model(appendModelPath)
        appendModel.trainable = False
        self.__getModel(hyperparameters, appendModel, revScalingX)
        history = self.Model.fit(self.Input(len(actual)), actual, batch_size=len(actual), verbose=0, epochs=1000, validation_split=0.2, callbacks=[EarlyStoppingValLoss])
        return MSE(actual, self.Model(self.Input(len(actual)), training=False).numpy()).numpy()
        
    def TuneHyperparameters(self, hyperparameters, appendModelPath, actual, revScalingDF_X):
        t = time.time()
        if os.path.exists(self.FilePath): shutil.rmtree(self.FilePath)
        os.makedirs(self.FilePath)

        df = pd.DataFrame(columns = ['Settings', 'Loss'])
        t_tuning = time.time()

        revScaling_X = GetScalingLayer(None, scaledDF=revScalingDF_X, reverse=True)

        for i, hp in hyperparameters.iterrows():
            print (f'Hyperparameters\t:{dict(hp)}')
            loss = self.__trainModel(hp, appendModelPath, actual, revScaling_X)
            df.loc[i] = [[str(x) for x in hp.values], loss]
            self.Generator.save(f"{self.FilePath}/G{i}.h5")
            self.Model.save(f"{self.FilePath}/M{i}.h5")

            print (f'Current Set\t: {(time.time()-t_tuning):.0f} seconds')
            print (f'Validation Loss\t: {loss}')
            t_tuning = time.time()

            df.sort_values(by='Loss', inplace=True)
            df.to_csv(f'{self.FilePath}/tuning.csv')
            
        print (f'Hyperparameter Tuning\t: {(t_tuning-t):.0f} seconds')

        df.sort_values(by='Loss', inplace=True)
        df.to_csv(f'{self.FilePath}/tuning.csv')

    def Predict(self, numSamples, numModels=1, mean=True, seed=0):
        '''
            makes predictions using the ML model
        '''
        tuning = pd.read_csv(f'{self.FilePath}/tuning.csv', index_col=0)
        dfs = pd.DataFrame(columns=self.Parameters)

        numModels = min(len(tuning), numModels)
        for m in tuning.index[:numModels]:
            model = load_model(f'{self.FilePath}/G{m}.h5')
            prediction = model(self.Input(numSamples), training=False).numpy()
            if mean:
                dfs.loc[f'G{m}'] = prediction.mean(axis=0)
            else:
                for i, p in enumerate(prediction):
                    dfs.loc[f'G{m}-{i}'] = p
        return dfs