import time
import numpy as np
import Manager as manager
import Tools.Computations as computer
import Class.NetworkBuilder as builder
import Class.Model as model
import TestLibraryFunction as tests

# import keras
# from keras import layers

# 1 - Program
# 2 - Tests
# 0 - ExecConsole

launch = 2

# Program
if launch == 1:
    start = time.time()

    # Get dataset from openML
    dataset_id = 40996
    feature_name = 'class',
    normalization_constant = 255
    batch_size = 100
    ds_inputs, ds_targets = manager.get_dataset(dataset_id, feature_name, normalization_constant, batch_size=batch_size)

    input_size = np.shape(ds_inputs[0][0])[0]
    output_size = np.shape(ds_targets[0][0])[0]
    # Choose hidden layer sizes
    hidden_layer_sizes = [800, 264, 32]

    # Build network
    network_builder = builder.NetworkBuilder(input_size, output_size)
    for layer_size in hidden_layer_sizes:
        # network_builder.add_dense_layer(layer_size, 'tan_h')
        network_builder.add_dense_layer(layer_size, 'relu', normalization_function='norm_2')

    # Output layer bloc (dense + OneToOne softmax)
    network_builder.add_dense_layer(output_size, 'sigmoid', is_output_layer=True, use_bias=False, normalization_function='')
    network_builder.add_one_to_one_layer(output_size, 'softmax')

    network = network_builder.build()

    # Setup train model
    model = model.ModelParameters(
        computer.cross_entropy,
        computer.distance_get,
        initial_learning_rate=0.1,
        final_learning_rate=0.01,
        learning_rate_steps=20,
        epochs=50)

    # Run model
    pre_train_test_result, train_batch_cost_fct, post_train_test_result = manager.train_network(ds_inputs, ds_targets, network, model)

    # Plot results
    manager.plot_result(pre_train_test_result, train_batch_cost_fct, post_train_test_result)

    tick = time.time()
    print('Execution time batch_size = {0} : {1}'.format(batch_size, tick - start))


# test
elif launch == 2:
    start = time.time()
    tests.test_dense_1_hidden('relu', 'norm_2')
    tick = time.time()
    print('Execution of case {0} in {1} s'.format(launch, tick - start))


# Exec console
else:
    print("")
