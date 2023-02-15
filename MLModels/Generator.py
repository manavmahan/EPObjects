from functools import reduce
import glob
import numpy as np
import os
import pandas as pd
import shutil
import tensorflow as tf

from MLModels.MLModel import EarlyStopping

class Generator():
    def __init__(self, numInputs, parameters, filePath):
        self.NumInputs = numInputs
        self.NumOutputs = len(parameters)
        self.Parameters = parameters
        self.FilePath = filePath

    def __createModel(self, hyperparameters, appendModel, revScalingX):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.InputLayer(input_shape = (self.NumInputs, )))

        for nn in [n for n in hyperparameters['NN'] if n>0]:
            model.add( tf.keras.layers.Dense(nn, 
                                           activation=tf.keras.activations.relu,) )

        model.add(tf.keras.layers.Dense(self.NumOutputs,))
        model.add(revScalingX)
        self.Generator = model
        outputs = appendModel(self.Generator.output)
        self.Model = tf.keras.Model(inputs=self.Generator.inputs, outputs=outputs)
        self.Model.compile(loss=tf.keras.losses.mean_squared_error, optimizer=tf.keras.optimizers.Adam(learning_rate=hyperparameters['LR']))

    def __trainModel(self, hyperparameters, appendModelPath, actual, revScalingX):
        '''
        training ANN model based on the hyperparameters
        '''
        appendModel = tf.keras.models.load_model(appendModelPath)
        appendModel.trainable = False

        loss = tf.keras.losses.MeanSquaredError()
        self.__createModel(hyperparameters, appendModel, revScalingX)
        self.Model.fit(tf.random.normal((len(actual), self.NumInputs)), actual, verbose=1, epochs=1000, validation_split=0.2, callbacks=[EarlyStopping])
        return loss(actual, self.Model(tf.random.normal([len(actual), self.NumInputs]), training=False)).numpy()
        
    def TuneHyperparameters(self, hyperparameters, appendModelPath, actual, revScalingX):
        path = self.FilePath
        if os.path.exists(path): shutil.rmtree(path)
        os.makedirs(path)

        df = pd.DataFrame(columns = ['Settings', 'Loss'])
        for i, hp in hyperparameters.iterrows():
            tf.keras.backend.clear_session()
            loss = self.__trainModel(hp, appendModelPath, actual, revScalingX)
            df.loc[i] = [[str(x) for x in hp.values], loss]
            self.Generator.save(f"{path}/G{i}.h5")
            self.Model.save(f"{path}/M{i}.h5")
            df.to_csv(f"{path}/tuning.csv")

    def Predict(self, numSamples, seed=0):
        '''
        makes predictions using the ML model
        '''
        dfs = pd.DataFrame(columns=self.Parameters)
        for modelPath in (glob.glob(f'{self.FilePath}/G*.h5')):
            model = tf.keras.models.load_model(modelPath)
            prediction = model(tf.random.normal([numSamples, self.NumInputs],), training=False).numpy().mean(axis=0)
            dfs.loc[modelPath] = prediction
        return dfs