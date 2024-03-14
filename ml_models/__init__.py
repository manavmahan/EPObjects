import math
import numpy as np
import pandas as pd

from tensorflow.keras.activations import relu, hard_sigmoid
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Activation, Dense, InputLayer, Rescaling, Layer
from tensorflow.keras.losses import Loss, mean_squared_error
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import L2, Regularizer
from tensorflow.keras.utils import register_keras_serializable
from tensorflow.keras import Model, Sequential
from tensorflow import math

early_stopping_loss = EarlyStopping(monitor='loss', min_delta=1e-04, patience=10, restore_best_weights=True,)
early_stopping_validation_loss = EarlyStopping(monitor='val_loss', min_delta=1e-04, patience=20, restore_best_weights=True,)

@register_keras_serializable(package='Custom', name='RegularizerHS')
class RegularizerHS(Regularizer):
    def __init__(self, l2=100):
        self.l2 = l2

    def __call__(self, x):
        x = math.log(abs(math.multiply(x, 0.4)))
        x = math.add(x, abs(x))
        return math.reduce_mean(math.multiply(x, self.l2))

    def get_config(self):
        return {'l2': float(self.l2)}


def get_scaling_layer(scaled_df: pd.DataFrame=None, 
                      reverse: bool=False,)->Rescaling:
    """ Return (min-max) scaling layer based on scaled_df. """
    if reverse:
        return Rescaling(scaled_df['Range'].values, offset = scaled_df['Min'].values)
    else:
        return Rescaling(1./scaled_df['Range'].values, offset = (-scaled_df['Min']/scaled_df['Range']).values)


def get_scaling_parameters(
        dataset: pd.DataFrame, 
        all_columns_equal: bool)-> pd.DataFrame:
    """ Calulates a dataframe for a min-max scaling layer based on the dataset. """
    df = pd.DataFrame(index = dataset.columns)
    df['Min'] = dataset.min(axis=0) 
    df['Max'] = dataset.max(axis=0)
    if all_columns_equal:
        df['Min'] = df['Min'].values.min() * np.ones(len(dataset.columns))
        df['Max'] = df['Max'].values.max() * np.ones(len(dataset.columns))
    df['Range'] = df['Max'] - df['Min']
    return df


def get_simple_ann(
        hyperparameters: pd.DataFrame, 
        num_inputs: int, 
        num_outputs: int, 
        scaling_X: Rescaling, 
        inverted: bool=False)->Sequential:
    """ Get a simple ANN based on hyperparameter, number of inputs/outputs, and scaling layers."""
    model = Sequential()
    model.add(InputLayer(input_shape = (num_inputs, )))
    model.add(scaling_X)
    hidden_layers = list(n for n in hyperparameters['num_neurons'] if n>0)
    for nn in hidden_layers:
        model.add( Dense(nn, activation=relu, kernel_regularizer=L2(hyperparameters['reg_coef'])) )

    model.add(Dense(num_outputs, activity_regularizer=RegularizerHS() if inverted else None))
    return model

from tensorflow import reduce_min
class LossMinimum(Loss):
    def __init__(self, error_fn=mean_squared_error):
        super(LossMinimum, self).__init__()
        self.error_fn = error_fn
    
    def call(self, y_true, y_pred):
        return reduce_min(self.error_fn(y_pred, y_true), axis=-1)
    
def train_model(model, X_train, Y_train, learning_rate, loss=mean_squared_error)-> float:
    """ Trains a sequential model based on the dataset. """
    model.compile(loss=loss, optimizer=Adam(learning_rate=learning_rate, amsgrad=True))
    history = model.fit(X_train, Y_train, 
                        validation_split=0.2, 
                        epochs=1000, verbose=0, 
                        callbacks=[early_stopping_validation_loss], 
                        batch_size=len(X_train))
    return min(history.history['val_loss'])


def get_regressor(hp, X, Y, scaling_df_X, scaling_df_Y, inverted=False):
    scaling_X = get_scaling_layer(scaled_df=scaling_df_X)
    scaling_Y = get_scaling_layer(scaled_df=scaling_df_Y)
    Y_scaled = scaling_Y(Y).numpy()
    
    ann = get_simple_ann(hp, len(X.iloc[0]), len(Y.iloc[0]), scaling_X, inverted=inverted)
    if inverted: ann.add(Activation(hard_sigmoid))
    loss = train_model(ann, X, Y_scaled, hp['learning_rate'])
    if inverted: ann.add(get_scaling_layer(scaled_df=scaling_df_Y, reverse=True))
    return ann, loss


def get_random_input(num_examples, num_dims):
    return np.random.randn(num_examples, num_dims)


def get_generator_network(hyperparameters, append_model, input_dims, output_dims, rev_scaling_X,):
    append_model.trainable = False
    generator = Sequential()
    generator.add(InputLayer(input_shape = (input_dims, )))
    for nn in [n for n in hyperparameters['num_neurons'] if n>0]:
        generator.add(Dense(nn, kernel_regularizer=L2(hyperparameters['reg_coef']), activation=relu,))

    generator.add(Dense(output_dims, activity_regularizer=RegularizerHS()))
    generator.add(Activation(hard_sigmoid))
    generator.add(rev_scaling_X)

    outputs = append_model(generator.output)
    complete_model = Model(inputs=generator.inputs, outputs=outputs)
    return generator, complete_model


def get_generator(hp, scaling_df_X, regressor, targets):
    rev_scaling_X = get_scaling_layer(scaled_df=scaling_df_X, reverse=True)
    random_input = get_random_input(len(targets), 1000) * 50

    output_dims = len(scaling_df_X)
    generator, complete_model = get_generator_network(hp, regressor, len(random_input[0]), output_dims, rev_scaling_X,)
    loss = train_model(complete_model, random_input, targets, hp['learning_rate'])
    return generator, loss


def predict(model, X=None, num_examples=1):
    if X is None:
        config = model.get_config()
        X = get_random_input(num_examples, config["layers"][0]["config"]["batch_input_shape"][1])
    return model(X, training=False).numpy()
