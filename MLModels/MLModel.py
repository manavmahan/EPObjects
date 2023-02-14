from functools import reduce
import numpy as np
import os
import pandas as pd
import shutil
import tensorflow as tf

EarlyStopping = tf.keras.callbacks.EarlyStopping(min_delta=1e-05, 
                                                 patience=20, 
                                                 restore_best_weights=True,)

def Multiply(tup):
    return reduce(lambda x, y: x * y if x and y else x if x else y, tup)

def GetScalingLayer(dataset, reverse=False, allColumnsEqual=False):
    scaledDF = GetScalingParameters(dataset) if not allColumnsEqual else GetScalingParametersAllColumnsEqual(dataset)
    if reverse:
        return tf.keras.layers.Rescaling(scaledDF['Range'].values, offset = scaledDF['Min'].values)
    else:
        return tf.keras.layers.Rescaling(1./scaledDF['Range'].values, offset = (-scaledDF['Min']/scaledDF['Range']).values)

def GetScalingParameters(dataDF):
    df = pd.DataFrame(index = dataDF.columns)
    df['Min'] = dataDF.min(axis=0)
    df['Max'] = dataDF.max(axis=0)
    df['Range'] = df['Max'] - df['Min']
    return df

def GetScalingParametersAllColumnsEqual(dataDF):
    df = pd.DataFrame(index = dataDF.columns)
    df['Min'] = dataDF.values.min() * np.ones(len(dataDF.columns))
    df['Max'] = dataDF.values.max() * np.ones(len(dataDF.columns))
    df['Range'] = df['Max'] - df['Min']
    return df

class Regressor():
    def __init__(self, inputs, outputs, filePath):
        self.Inputs = inputs
        self.Outputs = outputs
        self.NumInputs = len(self.Inputs)
        self.NumOutputs = len(self.Outputs)
        self.FilePath = filePath

    def __createModel(self, hyperparameters, scalingX, revScalingY=None):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.InputLayer(input_shape = (self.NumInputs, )))
        model.add(scalingX)

        for nn in [n for n in hyperparameters['NN'] if n>0]:
            model.add( tf.keras.layers.Dense(nn, 
                                           activation=tf.keras.activations.relu, 
                                           kernel_regularizer=tf.keras.regularizers.L2(hyperparameters['RC'])) )

        model.add(tf.keras.layers.Dense(self.NumOutputs))
        # if revScalingY is not None: model.add(revScalingY)
        
        model.compile(loss=tf.keras.losses.mean_squared_error, optimizer=tf.keras.optimizers.Adam(learning_rate=hyperparameters['LR']),)
        model.summary()
        return model

    def __trainModel(self, hyperparameters, X, Y, scalingX, revScalingY=None):
        '''
        training ANN model based on the hyperparameters
        '''        
        model = self.__createModel(hyperparameters, scalingX, revScalingY)
        model.fit(X, Y, validation_split=0.2, epochs=1000, verbose=0, callbacks=[EarlyStopping],)

        loss = tf.keras.losses.MeanSquaredError()
        return model, loss( model(X, training=False), Y).numpy()
        
    def TuneHyperparameters(self, hyperparametersSet, X, Y):
        path = f'{self.FilePath}/Tuning'
        if os.path.exists(path): shutil.rmtree(path)
        os.makedirs(path)

        df = pd.DataFrame(columns = ['Settings', 'Loss'])
            
        scalingX = GetScalingLayer(X)
        scalingY = GetScalingLayer(Y, True, True)
        for i, hp in hyperparametersSet.iterrows():
            tf.keras.backend.clear_session()
            model, loss = self.__trainModel(hp, X.values, Y.values, scalingX, scalingY)
            df.loc[i] = [[str(x) for x in hp.values], loss]
            model.save(f"{path}/M{i}.h5")
            df.to_csv(f"{path}/tuning.csv")
                
        # copy the best fit model to the model location
        df = pd.read_csv(f"{path}/tuning.csv", index_col=0)
        m = df["Loss"].idxmin()
        shutil.copyfile(f"{path}/M{i}.h5", f"{self.FilePath}.h5")  

    def Predict(self, data,):
        '''
        makes predictions using the ML model
        '''
        model = tf.keras.models.load_model(f"{self.FilePath}.h5")
        predictedY = model.predict(data[self.Inputs], verbose=0)
        data[[f"Predicted_{x}" for x in self.Outputs]] = predictedY
        return data