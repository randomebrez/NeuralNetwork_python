import numpy as np
from tensorflow import keras
from keras import layers
import Tools.OpenmlGateway as openMl
import Tools.PlotHelper as ph

dataset_id = 40996
input_shape = (28, 28)
column_shape = 28 * 28
feature_name = 'class'
class_number = 10
batch_size = 100

def perceptron():
    ds_train, ds_test = openMl.get_keras_dataset(dataset_id, feature_name, batch_size)
    # Build model
    inputs = keras.Input(shape=column_shape)
    x = layers.Rescaling(1.0 / 255)(inputs)
    for size in [700]:
        x = layers.Dense(size, "relu", name="dense_1")(x)
    outputs = layers.Dense(class_number, activation="softmax", name="dense_2")(x)

    model = keras.Model(inputs, outputs)

    # Config of model with losses and metrics
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Model training
    epochs = 25
    model.fit(
        ds_train,
        epochs=epochs,
        shuffle=True,
        validation_data=ds_test
    )

    # Evaluate Model
    model.evaluate(ds_test)

def auto_encoder():
    ds_train, ds_test = openMl.get_keras_dataset_auto_encoder(dataset_id, feature_name, batch_size)

    # Build model
    inputs = keras.Input(shape=column_shape)
    x = layers.Rescaling(1.0 / 255)(inputs)

    layer_sizes = [700, 100, 700]
    for index, size in enumerate(layer_sizes):
        x = layers.Dense(size, "relu", name="dense_{0}".format(index))(x)

    outputs = layers.Dense(np.product(np.asarray(input_shape)), activation="relu", name="dense_{0}".format(len(layer_sizes)))(x)

    model = keras.Model(inputs, outputs)

    # Config of model with losses and metrics
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="mean_squared_error",
        metrics=["accuracy"],
    )

    # Model training
    epochs = 20
    model.fit(
        ds_train,
        epochs=epochs,
        shuffle=True,
        validation_data=ds_test
    )

    ph.plot_keras_auto_encoder_results(model, ds_test, 36)

def convolution():
    ds_train, ds_test = openMl.get_keras_dataset_convolution(dataset_id, feature_name, batch_size)

    # Build model
    inputs = keras.Input(shape=(28, 28, 1))
    x = layers.Rescaling(1.0 / 255)(inputs)

    x = layers.Convolution2D(3, 6, 2)(x)
    x = layers.MaxPool2D()(x)
    x = layers.Flatten()(x)
    x = layers.Dense(800, "relu", name="middle_dense")(x)

    outputs = layers.Dense(class_number, activation="softmax", name="outputs")(x)

    model = keras.Model(inputs, outputs)

    # Config of model with losses and metrics
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Model training
    epochs = 20
    model.fit(
        ds_train,
        epochs=epochs,
        shuffle=True,
        validation_data=ds_test
    )