import numpy as np
import pandas as pd

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

early_stopping_loss = EarlyStopping(monitor='loss', min_delta=1e-05, patience=1, restore_best_weights=True,)
early_stopping_validation_loss = EarlyStopping(monitor='val_loss', min_delta=1e-05, patience=20, restore_best_weights=True,)

def get_scaling_layer(dataset:pd.DataFrame = None, 
                      scaled_df:pd.DataFrame=None, 
                      reverse:bool=False, 
                      all_columns_equal:bool=False)->Rescaling:
    """ Return (min-max) scaling layer based on dataset or scaled_df. """
    if scaled_df is None: scaled_df = get_scaling_parameters(dataset, all_columns_equal)
    if reverse:
        return Rescaling(scaled_df['Range'].values, offset = scaled_df['Min'].values)
    else:
        return Rescaling(1./scaled_df['Range'].values, offset = (-scaled_df['Min']/scaled_df['Range']).values)

def get_scaling_parameters(
        dataset:pd.DataFrame, 
        all_columns_equal:bool)-> pd.DataFrame:
    """ Calulates a scaling dataframe for min-max scaling layer based on a dataset. """
    df = pd.DataFrame(index = dataset.columns)
    df['Min'] = dataset.values.min() * np.ones(len(dataset.columns)) if all_columns_equal else dataset.min(axis=0) 
    df['Max'] = dataset.values.max() * np.ones(len(dataset.columns)) if all_columns_equal else dataset.max(axis=0)
    df['Range'] = df['Max'] - df['Min']
    return df

def get_simple_ann(
        hyperparameters: pd.DataFrame, 
        num_inputs: int, 
        num_outputs: int, 
        scaling_X: Rescaling, 
        rev_scaling_Y: Rescaling)->Sequential:
    """ Get a simple ANN based on hyperparameter, number of inputs/outputs, and scaling layers."""
    model = Sequential()
    model.add(InputLayer(input_shape = (num_inputs, )))
    model.add(scaling_X)
    
    for nn in (n for n in hyperparameters['num_neurons'] if n>0):
        model.add( Dense(nn, activation=relu, kernel_regularizer=L2(hyperparameters['reg_coeff'])) )

    model.add(Dense(num_outputs))
    model.add(rev_scaling_Y)
    
    model.compile(loss=mean_squared_error, optimizer=Adam(learning_rate=hyperparameters['learning_rate']),)
    return model

def train_model(model: Sequential, X_train: np.ndarray, Y_train: np.ndarray,)-> float:
    """ Trains a sequential model based on the dataset. """
    history = model.fit(X_train, Y_train, validation_split=0.2, epochs=10, verbose=0, callbacks=[early_stopping_validation_loss],)
    return min(history.history['val_loss']) 

def get_regressor(hyperparameters_df, X, Y, scaling_df_X=None):
    scaling_X = get_scaling_layer(X, scaling_df_X)
    scaling_Y = get_scaling_layer(Y, all_columns_equal=False, reverse=True)

    current_model, current_loss = None, float('inf')
    for _, hp in hyperparameters_df.iterrows():
        ann = get_simple_ann(hp, len(X.iloc[0]), len(Y.iloc[0]), scaling_X, scaling_Y)
        loss = train_model(ann, X, Y,)
        if loss < current_loss:
            current_loss = loss
            current_model = ann
    return current_model, current_loss

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
    generator = Sequential()
    generator.add(InputLayer(input_shape = (input_dims, )))

    for nn in [n for n in hyperparameters['num_neurons'] if n>0]:
        generator.add( Dense(nn, kernel_regularizer=L2(hyperparameters['reg_coeff']), activation=sigmoid,))

    generator.add(Dense(output_dims, activity_regularizer=CustomRegularizerHardSigmoid()))
    generator.add(Activation(hard_sigmoid))
    generator.add(rev_scaling_X)

    outputs = append_model(generator.output)
    complete_model = Model(inputs=generator.inputs, outputs=outputs)
    complete_model.compile(loss=CustomLossMinimum(), optimizer=Adam(learning_rate=hyperparameters['learning_rate']))
    return generator, complete_model

def get_generator(hyperparameters_df, scaling_df_X, regressor, targets):
    rev_scaling_X = get_scaling_layer(None, scaling_df_X, reverse=True)
    random_input = get_random_input(len(targets), 100)

    output_dims = len(scaling_df_X)
    for _, hp in hyperparameters_df.iterrows():
        generator, complete_model = get_generator_network(hp, regressor, len(random_input[0]), output_dims, rev_scaling_X)
        loss = train_model(complete_model, random_input, targets,)
        yield generator, loss

def predict(model_json, X=None, num_examples=1):
    model = model_from_json(model_json)
    if X is None:
        config = model.get_config()
        X = get_random_input(num_examples, config["layers"][0]["config"]["batch_input_shape"][1])
    return model.predict(X)