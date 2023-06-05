import math
import numpy as np
import pandas as pd

from tensorflow.keras.activations import relu, sigmoid, hard_sigmoid
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Activation, Dense, InputLayer, Rescaling, Layer
from tensorflow.keras.losses import Loss, mean_squared_error, BinaryCrossentropy, binary_crossentropy
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import L2, Regularizer
from tensorflow.keras.utils import register_keras_serializable
from tensorflow.keras import Model, Sequential
from tensorflow import math, ones_like, multiply
from tensorflow import reduce_min, where, reduce_sum
from tensorflow_probability import distributions

early_stopping_loss = EarlyStopping(monitor='loss', min_delta=1e-05, patience=1, restore_best_weights=True,)
early_stopping_validation_loss = EarlyStopping(monitor='val_loss', min_delta=1e-05, patience=20, restore_best_weights=True,)

def get_scaling_layer(dataset: pd.DataFrame=None, 
                      scaled_df: pd.DataFrame=None, 
                      reverse: bool=False, 
                      all_columns_equal: bool=False)->Rescaling:
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
        rev_scaling_Y: Rescaling,
        inverted: bool=False)->Sequential:
    """ Get a simple ANN based on hyperparameter, number of inputs/outputs, and scaling layers."""
    model = Sequential()
    model.add(InputLayer(input_shape = (num_inputs, )))
    model.add(scaling_X)
    
    hidden_layers = list(n for n in hyperparameters['num_neurons'] if n>0)
    for i, nn in enumerate(hidden_layers):
        model.add( Dense(nn, activation=relu, kernel_regularizer=L2(hyperparameters['reg_coeff'])) )

    model.add(Dense(num_outputs, activity_regularizer=CustomRegularizerHardSigmoid() if inverted else None))
    if inverted: model.add(Activation(hard_sigmoid))

    model.add(rev_scaling_Y)

    model.compile(loss=mean_squared_error, optimizer=Adam(learning_rate=hyperparameters['learning_rate']),)
    return model

def train_model(model: Sequential, X_train: np.ndarray, Y_train: np.ndarray,)-> float:
    """ Trains a sequential model based on the dataset. """
    history = model.fit(X_train, Y_train, validation_split=0.2, epochs=100, verbose=0, callbacks=[early_stopping_validation_loss],)
    return min(history.history['val_loss']) 

def get_regressor(hyperparameters_df, X, Y, scaling_df_X=None, scaling_df_Y=None, all_columns_equal=False, inverted=False):
    '''
    all_columns_equal has no effect if scaling_df_Y is provided.
    '''
    scaling_X = get_scaling_layer(X, scaling_df_X)
    scaling_Y = get_scaling_layer(Y, scaling_df_Y, reverse=True, all_columns_equal=all_columns_equal)

    current_model, current_loss = None, float('inf')
    for _, hp in hyperparameters_df.iterrows():
        ann = get_simple_ann(hp, len(X.iloc[0]), len(Y.iloc[0]), scaling_X, scaling_Y, inverted=inverted)
        loss = train_model(ann, X, Y,)
        while math.is_nan(loss):
            ann.summary()
            print (X, Y, scaling_X.weights, scaling_Y.weights, all_columns_equal, inverted, loss)
            ann = get_simple_ann(hp, len(X.iloc[0]), len(Y.iloc[0]), scaling_X, scaling_Y, inverted=inverted)
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
        x = math.log(abs(math.multiply(x, 0.4)))
        x = math.add(x, abs(x))
        return math.reduce_mean(math.multiply(x, self.l2))

    def get_config(self):
        return {'l2': float(self.l2)}

class LossMinimum(Loss):
    def __init__(self, error_fn=mean_squared_error):
        super(LossMinimum, self).__init__()
        self.error_fn = error_fn
    
    def call(self, y_true, y_pred):
        return reduce_min(self.error_fn(y_pred, y_true), axis=-1)
    
class LossErrorDomain(Loss):
    def __init__(self, error,):
        super(LossErrorDomain, self).__init__()
        self.error_domain = error

    def call(self, y_true, y_pred):
        errors = abs((y_pred - y_true) / y_true)
        actual = ones_like(errors)

        # probability = where(errors <= self.error_domain, 1., 0.)
        dist = distributions.Normal(loc=0., scale=self.error_domain)
        probability = 2 * (1 - dist.cdf(1.96 * abs(errors)))
        return reduce_min(binary_crossentropy(actual, probability), axis=-1)

def get_random_input(num_examples, num_dims):
    return np.random.random((num_examples, num_dims)) * 100

def get_generator_network(hyperparameters, append_model, input_dims, output_dims, rev_scaling_X, error_domain=None, ):
    append_model.trainable = False
    generator = Sequential()
    generator.add(InputLayer(input_shape = (input_dims, )))

    for nn in [n for n in hyperparameters['num_neurons'] if n>0]:
        generator.add( Dense(nn, kernel_regularizer=L2(hyperparameters['reg_coeff']), activation=sigmoid,))

    generator.add(Dense(output_dims, activity_regularizer=CustomRegularizerHardSigmoid()))
    generator.add(Activation(hard_sigmoid))
    generator.add(rev_scaling_X)

    outputs = append_model(generator.output)
    if error_domain:
        loss = LossErrorDomain(error_domain)
    else:
        loss = LossMinimum()

    complete_model = Model(inputs=generator.inputs, outputs=outputs)
    complete_model.compile(loss=loss, optimizer=Adam(learning_rate=hyperparameters['learning_rate']))
    return generator, complete_model

def get_generator(hyperparameters_df, scaling_df_X, regressor, targets, error_domain=None):
    rev_scaling_X = get_scaling_layer(None, scaling_df_X, reverse=True)
    random_input = get_random_input(len(targets), 20)

    output_dims = len(scaling_df_X)
    for _, hp in hyperparameters_df.iterrows():
        generator, complete_model = get_generator_network(hp, regressor, len(random_input[0]), output_dims, rev_scaling_X, error_domain=error_domain)
        loss = train_model(complete_model, random_input, targets,)
        yield generator, loss

def predict(model, X=None, num_examples=1):
    if X is None:
        config = model.get_config()
        X = get_random_input(num_examples, config["layers"][0]["config"]["batch_input_shape"][1])
    return model(X, training=False).numpy()