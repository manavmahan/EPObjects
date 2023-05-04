import numpy as np
import os
import pandas as pd
import shutil

from tensorflow.keras.activations import relu, sigmoid, hard_sigmoid
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Activation, Dense, InputLayer, Rescaling
from tensorflow.keras.losses import Loss, mean_squared_error
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import L2, Regularizer
from tensorflow.keras.utils import register_keras_serializable
from tensorflow.keras import Model, Sequential
from tensorflow.math import square, add, log, abs, multiply, reduce_mean 
from tensorflow import reduce_min

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
    
    for nn in (n for n in hyperparameters['num_neurons'] if n>0):
        model.add( Dense(nn, activation=relu, kernel_regularizer=L2(hyperparameters['reg_coeff'])) )

    model.add(Dense(num_outputs))
    model.add(rev_scaling_Y)
    
    model.compile(loss=mean_squared_error, optimizer=Adam(learning_rate=hyperparameters['learning_rate']),)
    return model

def train_model(model, X_train, Y_train,):
    history = model.fit(X_train, Y_train, validation_split=0.2, epochs=1000, verbose=0, callbacks=[early_stopping_validation_loss],)
    return model, min(history.history['val_loss']) 

def get_regressor(hyperparameters_df, X, Y, scaling_df_X=None):
    scaling_X = get_scaling_layer(X, scaling_df_X)
    scaling_Y = get_scaling_layer(Y, allColumnsEqual=False, reverse=True)

    current_model, current_loss = None, float('inf')
    for _, hp in hyperparameters_df.iterrows():
        ann = get_simple_ann(hp, len(X.iloc[0]), len(Y.iloc[0]), scaling_X, scaling_Y)
        model, loss = train_model(ann, X, Y,)
        if loss < current_loss:
            current_loss = loss
            current_model = model
    return current_model.to_json(), current_loss

@register_keras_serializable(package='Custom', name='CustomRegularizerHardSigmoid')
class CustomRegularizerHardSigmoid(Regularizer):
    def __init__(self, l2=100):
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

def get_random_input(num_examples, num_dims):
    return np.random.random((num_examples, num_dims)) * 100

def get_generator_network(hyperparameters, append_model, input_dims, output_dims, rev_scaling_X):
    append_model.trainable = False
    model = Sequential()
    model.add(InputLayer(input_shape = (input_dims, )))

    for nn in [n for n in hyperparameters['num_neurons'] if n>0]:
        model.add( Dense(nn, kernel_regularizer=L2(hyperparameters['reg_coeff']), activation=sigmoid,))

    model.add(Dense(output_dims, activity_regularizer=CustomRegularizerHardSigmoid()))
    model.add(Activation(hard_sigmoid))
    model.add(rev_scaling_X)

    outputs = append_model(model.output)
    model = Model(inputs=model.inputs, outputs=outputs)
    model.compile(loss=CustomLossMinimum(), optimizer=Adam(learning_rate=hyperparameters['learning_rate']))
    return model

def get_generator(hyperparameters_df, scaling_df_X, regressor_json, targets):
    rev_scaling_X = get_scaling_layer(None, scaling_df_X, reverse=True)
    random_input = get_random_input(len(targets), 100)

    output_dims = len(scaling_df_X)
    regressor = model_from_json(regressor_json)
    for _, hp in hyperparameters_df.iterrows():
        gn = get_generator_network(hp, regressor, len(random_input[0]), output_dims, rev_scaling_X)
        model, loss = train_model(gn, random_input, targets,)
        yield model.to_json(), loss

def predict(model_json, X=None, num_examples=1):
    model = model_from_json(model_json)
    if X is None:
        config = model.get_config()
        X = get_random_input(num_examples, config["layers"][0]["config"]["batch_input_shape"][1])
    return model.predict(X)