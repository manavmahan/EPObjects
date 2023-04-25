import numpy as np
import os
import pandas as pd
import shutil

from sklearn.model_selection import train_test_split

from tensorflow.keras.activations import relu, sigmoid, hard_sigmoid

from tensorflow.keras.callbacks import EarlyStopping

from tensorflow.keras.layers import Activation, Dense, InputLayer, Rescaling

from tensorflow.keras.models import load_model

from tensorflow.keras.losses import mean_squared_error, MeanSquaredError

from tensorflow.keras.optimizers import Adam

from tensorflow.keras.regularizers import L2, Regularizer

from tensorflow.keras import Sequential

from tensorflow import _logging
_logging.disable(_logging.DEBUG)
_logging.disable(_logging.INFO)
_logging.disable(_logging.WARNING)

early_stopping_loss = EarlyStopping(monitor='loss', min_delta=1e-05, patience=20, restore_best_weights=True,)
early_stopping_validation_loss = EarlyStopping(monitor='val_loss', min_delta=1e-05, patience=20, restore_best_weights=True,)

def get_scaling_layer(dataset=None, scaledDF=None, reverse=False, allColumnsEqual=False):
    if scaledDF is None: scaledDF = get_scaling_parameters(dataset, allColumnsEqual)
    if reverse:
        return Rescaling(scaledDF['Range'].values, offset = scaledDF['Min'].values)
    else:
        return Rescaling(1./scaledDF['Range'].values, offset = (-scaledDF['Min']/scaledDF['Range']).values)

def get_scaling_parameters(dataDF, allColumnsEqual):
    df = pd.DataFrame(index = dataDF.columns)
    df['Min'] = dataDF.values.min() * np.ones(len(dataDF.columns)) if allColumnsEqual else dataDF.min(axis=0) 
    df['Max'] = dataDF.values.max() * np.ones(len(dataDF.columns)) if allColumnsEqual else dataDF.max(axis=0)
    df['Range'] = df['Max'] - df['Min']
    return df

def get_simple_ann(hyperparameters, num_inputs, num_outputs, scaling_X, rev_scaling_Y,):
    model = Sequential()
    model.add(InputLayer(input_shape = (num_inputs, )))
    model.add(scaling_X)
    
    for nn in (n for n in hyperparameters['NN'] if n>0):
        model.add( Dense(nn, activation=relu, kernel_regularizer=L2(hyperparameters['RC'])) )

    model.add(Dense(num_outputs))
    model.add(rev_scaling_Y)
    
    model.compile(loss=mean_squared_error, optimizer=Adam(learning_rate=hyperparameters['LR']),)
    return model

def train_network(model, X_train, Y_train, X_val, Y_val,):
    if X_val is None:
        mse = MeanSquaredError()
        history = model.fit(X_train, Y_train, epochs=1000, verbose=0, callbacks=[early_stopping_loss],)
        return model, mse(Y_train, model(X_train, training=False).numpy()).numpy()
    else:
        history = model.fit(X_train, Y_train, validation_data=[X_val, Y_val], epochs=1000, verbose=0, callbacks=[early_stopping_validation_loss],)
        return model, min(history.history['val_loss']) 

def get_regressor(hyperparameters_df, X, Y, scaling_df_X=None):
    scalingX = get_scaling_layer(X, scaling_df_X)
    scalingY = get_scaling_layer(Y, allColumnsEqual=False, reverse=True)

    current_model, current_loss = None, float('inf')
    for _, hp in hyperparameters_df.iterrows():
        X_train, X_val, X_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=0)
        model, loss = train_network(hp, X_train, X_train, X_val, Y_val, scalingX, scalingY)
        if loss < current_loss:
            current_loss = loss
            current_model = model
    return current_model.to_json(), current_loss