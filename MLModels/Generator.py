from functools import reduce
import numpy as np
import os
import pandas as pd
import shutil
import tensorflow as tf

from MLModels.MLModel import Regressor

def TrainRegressor(hyperparameters, X, Y, filePath):
    regressor = Regressor(X.columns, Y.columns, filePath)
    regressor.TuneHyperparameters(hyperparameters, X, Y)

@tf.function
def TrainStep(model, actual):
    noise = tf.random.normal([1000, model.NumInputs],)
    with tf.GradientTape() as gen_tape:
        predictions = model.Model(noise, training=True)
        gen_loss = tf.keras.losses.mean_squared_error(actual, predictions)
        gradients_of_generator = gen_tape.gradient(gen_loss, model.Model.trainable_variables)
        model.Optimiser.apply_gradients(zip(gradients_of_generator, model.Model.trainable_variables))

class Generator():
    def __init__(self, numInputs, numOutputs, filePath):
        self.NumInputs = numInputs
        self.NumOutputs = numOutputs
        self.FilePath = filePath

    def __createModel(self, hyperparameters, appendModel, revScalingX):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.InputLayer(input_shape = (self.NumInputs, )))

        for nn in [n for n in hyperparameters['NN'] if n>0]:
            model.add( tf.keras.layers.Dense(nn, 
                                           activation=tf.keras.activations.relu, 
                                           kernel_regularizer=tf.keras.regularizers.L2(hyperparameters['RC'])) )

        model.add(tf.keras.layers.Dense(self.NumOutputs))
        model.add(revScalingX)
        self.Generator = model
        outputs = appendModel(self.Generator.output)
        self.Model = tf.keras.Model(inputs=self.Generator.inputs, outputs=outputs)
        self.Model.compile(loss=tf.keras.losses.mean_squared_error)
        self.Optimiser = tf.keras.optimizers.Adam(learning_rate=hyperparameters['LR'])

    def __trainModel(self, hyperparameters, appendModelPath, actual, revScalingX):
        '''
        training ANN model based on the hyperparameters
        '''
        appendModel = tf.keras.models.load_model(appendModelPath)
        appendModel.trainable = False

        self.__createModel(hyperparameters, appendModel, revScalingX)
        for _ in range(1000):
            TrainStep(self, actual)

        loss = tf.keras.losses.MeanSquaredError()
        return loss(actual, self.Model(tf.random.normal([len(actual), self.NumInputs]), training=False)).numpy()
        
    def TuneHyperparameters(self, hyperparameters, appendModelPath, actual, revScalingX):
        path = f'{self.FilePath}/Tuning'
        if os.path.exists(path): shutil.rmtree(path)
        os.makedirs(path)

        df = pd.DataFrame(columns = ['Settings', 'Loss'])
            
        i = 0
        for i, hp in hyperparameters.iterrows():
            tf.keras.backend.clear_session()
            loss = self.__trainModel(hp, appendModelPath, actual, revScalingX)
            df.loc[i] = [[str(x) for x in hp.values], loss]
            self.Generator.save(f"{path}/M{i}.h5")
            df.to_csv(f"{path}/tuning.csv")
                
        # copy the best fit model to the model location
        df = pd.read_csv(f"{path}/tuning.csv", index_col=0)
        m = df["Loss"].idxmin()
        shutil.copyfile(f"{path}/M{i}.h5", f"{self.FilePath}.h5")  

    def Predict(self, numSamples, seed=0):
        '''
        makes predictions using the ML model
        '''
        model = tf.keras.models.load_model(f"{self.FilePath}.h5")
        return model(tf.random.normal([numSamples, self.NumInputs], seed=seed), training=False).numpy()