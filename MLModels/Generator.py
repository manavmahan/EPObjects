from functools import reduce
import glob
import numpy as np
import os
import pandas as pd
import shutil

from MLModels.Regressor import Activation, Adam, Dense, EarlyStoppingValLoss, L2, Sequential, InputLayer, mean_squared_error, MSE, Regularizer, Rescaling, relu, load_model, sigmoid, hard_sigmoid

from tensorflow.random import normal
from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras.utils import get_custom_objects
from tensorflow.keras.utils import register_keras_serializable
from tensorflow.math import add, log, abs, multiply, subtract, reduce_mean

@register_keras_serializable(package='Custom', name='CustomRegularizer')
class CustomRegularizer(Regularizer):
    def __init__(self, l2=0.001):
        self.l2 = l2

    def __call__(self, x):
        x = log(abs(multiply(subtract(x, 0.5), 2)))
        x = add(x, abs(x))
        return reduce_mean(multiply(x, self.l2))

    def get_config(self):
        return {'l2': float(self.l2)}

class Generator():
    def __init__(self, numInputs, parameters, filePath):
        self.NumInputs = numInputs
        self.NumOutputs = len(parameters)
        self.Parameters = parameters
        self.FilePath = filePath

    def __getModel(self, hyperparameters, appendModel, revScalingX):
        model = Sequential()
        model.add(InputLayer(input_shape = (self.NumInputs, )))

        for nn in [n for n in hyperparameters['NN'] if n>0]:
            model.add( Dense(nn, kernel_regularizer=L2(hyperparameters['RC'])), activation=sigmoid,)

        model.add(Dense(self.NumOutputs, activity_regularizer=CustomRegularizer()))
        model.add(Activation(sigmoid))
        model.add(revScalingX)

        self.Generator = model
        outputs = appendModel(self.Generator.output)
        self.Model = Model(inputs=self.Generator.inputs, outputs=outputs)
        self.Model.compile(loss=mean_squared_error, optimizer=Adam(learning_rate=hyperparameters['LR']))

    def __trainModel(self, hyperparameters, appendModelPath, actual, revScalingX):
        appendModel = load_model(appendModelPath)
        appendModel.trainable = False
        self.__getModel(hyperparameters, appendModel, revScalingX)
        history = self.Model.fit(normal((len(actual), self.NumInputs)), actual, batch_size=len(actual), verbose=1, epochs=1000, validation_split=0.2, callbacks=[EarlyStoppingValLoss])
        return MSE(actual, self.Model(normal([len(actual), self.NumInputs],), training=False).numpy()).numpy()
        
    def TuneHyperparameters(self, hyperparameters, appendModelPath, actual, revScalingX):
        if os.path.exists(self.FilePath): shutil.rmtree(self.FilePath)
        os.makedirs(self.FilePath)

        df = pd.DataFrame(columns = ['Settings', 'Loss'])
        for i, hp in hyperparameters.iterrows():
            loss = self.__trainModel(hp, appendModelPath, actual, revScalingX)
            df.loc[i] = [[str(x) for x in hp.values], loss]
            self.Generator.save(f"{self.FilePath}/G{i}.h5")
            self.Model.save(f"{self.FilePath}/M{i}.h5")

        df.sort_values(by='Loss', inplace=True)
        for i in df.index[:int(len(df)//2)]:
            os.remove(f"{self.FilePath}/G{i}.h5")
            os.remove(f"{self.FilePath}/M{i}.h5")
    
    def Predict(self, numSamples, seed=0):
        '''
            makes predictions using the ML model
        '''
        dfs = pd.DataFrame(columns=self.Parameters)
        for modelPath in (glob.glob(f'{self.FilePath}/G*.h5')):
            model = load_model(modelPath)
            prediction = model(normal([numSamples, self.NumInputs],), training=False).numpy()
            for i, p in enumerate(prediction):
                dfs.loc[f'{modelPath}-{i}'] = p
        return dfs.sample(frac=1)