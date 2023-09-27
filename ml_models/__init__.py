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

early_stopping_loss = EarlyStopping(monitor='loss', min_delta=1e-04, patience=1, restore_best_weights=True,)
early_stopping_validation_loss = EarlyStopping(monitor='val_loss', min_delta=1e-04, patience=20, restore_best_weights=True,)

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
        inverted: bool=False)->Sequential:
    """ Get a simple ANN based on hyperparameter, number of inputs/outputs, and scaling layers."""
    model = Sequential()
    model.add(InputLayer(input_shape = (num_inputs, )))
    model.add(scaling_X)
    
    hidden_layers = list(n for n in hyperparameters['num_neurons'] if n>0)
    for i, nn in enumerate(hidden_layers):
        model.add( Dense(nn, activation=relu, kernel_regularizer=L2(hyperparameters['reg_coef'])) )

    model.add(Dense(num_outputs, activity_regularizer=CustomRegularizerHardSigmoid() if inverted else None))
    return model

def train_model(model: Sequential, X_train: np.ndarray, Y_train: np.ndarray, learning_rate, loss=None)-> float:
    """ Trains a sequential model based on the dataset. """
    if loss is None:
        loss = mean_squared_error
    model.compile(loss=loss, optimizer=Adam(learning_rate=learning_rate, amsgrad=True))
    history = model.fit(X_train, Y_train, validation_split=0.2, epochs=1000, verbose=0, callbacks=[early_stopping_validation_loss],)
    return min(history.history['val_loss']), len(history.history['val_loss'])

def get_regressor(hyperparameters_df, X, Y, scaling_df_X=None, scaling_df_Y=None, all_columns_equal=True, inverted=False):
    '''
    all_columns_equal has no effect if scaling_df_Y is provided.
    '''
    scaling_X = get_scaling_layer(X, scaling_df_X)

    if scaling_df_Y is None: scaling_df_Y = get_scaling_parameters(Y, all_columns_equal=all_columns_equal) 
    scaling_Y = get_scaling_layer(Y, scaling_df_Y, all_columns_equal=all_columns_equal)

    Y_scaled = scaling_Y(Y).numpy()
    current_model, current_loss, current_epoch = None, float('inf'), 0
    for _, hp in hyperparameters_df.iterrows():
        ann = get_simple_ann(hp, len(X.iloc[0]), len(Y.iloc[0]), scaling_X, inverted=inverted)
        if inverted: ann.add(Activation(hard_sigmoid))
        loss, epoch = train_model(ann, X, Y_scaled, hp['learning_rate'])

        if loss < current_loss:
            current_loss = loss
            current_model = ann
            current_epoch = epoch
    if inverted: current_model.add(get_scaling_layer(scaled_df=scaling_df_Y, reverse=True))
    return current_model, scaling_df_Y, current_loss, current_epoch

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
        try:
            if len(self.error_domain) == 2: self.skewed = True
        except: self.skewed = False

    def call(self, y_true, y_pred):
        errors = (y_pred - y_true) / y_true
        actual = ones_like(errors)

        probability = where(abs(errors) <= self.error_domain[1], 1., (200.*self.error_domain[1] - abs(errors))/2000.*self.error_domain[1])
        if self.skewed:
            dist_left = distributions.Normal(loc=0., scale=-self.error_domain[0])
            dist_right = distributions.Normal(loc=0., scale=self.error_domain[1])
            probability = where(errors<0, 2 * (1 - dist_left.cdf(1.96 * abs(errors))), 2 * (1 - dist_right.cdf(1.96 * abs(errors))))
            # probability = where(self.error_domain[0] < errors < self.error_domain[1], 1., 0.)
        else:
            dist = distributions.Normal(loc=0., scale=self.error_domain)
            probability = 2 * (1 - dist.cdf(1.96 * abs(errors)))
            # probability = where(abs(errors)<self.error_domain, 1., 0.)
        return reduce_min(binary_crossentropy(actual, probability), axis=-1)

def get_random_input(num_examples, num_dims):
    return np.random.random((num_examples, num_dims)) * 100

def get_generator_network(hyperparameters, append_model, input_dims, output_dims, rev_scaling_X,):
    append_model.trainable = False
    generator = Sequential()
    generator.add(InputLayer(input_shape = (input_dims, )))

    for nn in [n for n in hyperparameters['num_neurons'] if n>0]:
        generator.add( Dense(nn, kernel_regularizer=L2(hyperparameters['reg_coef']), activation=sigmoid,))

    generator.add(Dense(output_dims, activity_regularizer=CustomRegularizerHardSigmoid()))
    generator.add(Activation(hard_sigmoid))
    generator.add(rev_scaling_X)

    outputs = append_model(generator.output)

    complete_model = Model(inputs=generator.inputs, outputs=outputs)
    return generator, complete_model

def get_generator(hyperparameters_df, scaling_df_X, regressor, targets, error_domain=None):
    rev_scaling_X = get_scaling_layer(None, scaling_df_X, reverse=True)
    random_input = get_random_input(len(targets), 20)

    output_dims = len(scaling_df_X)
    for _, hp in hyperparameters_df.iterrows():
        generator, complete_model = get_generator_network(hp, regressor, len(random_input[0]), output_dims, rev_scaling_X,)
        loss, epochs = train_model(complete_model, random_input, targets, hp['learning_rate'], LossErrorDomain(error_domain) if error_domain is not None else LossMinimum())
        yield generator, loss, epochs

def predict(model, X=None, num_examples=1):
    if X is None:
        config = model.get_config()
        X = get_random_input(num_examples, config["layers"][0]["config"]["batch_input_shape"][1])
    return model(X, training=False).numpy()