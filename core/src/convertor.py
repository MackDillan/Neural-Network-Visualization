import keras

from core.src.models import Topology, Layer, Neuron, Connection


def convert(model: keras.Sequential) -> Topology:
    neuron_counter = 0  # Counter for unique neuron identifiers
    nn = Topology()
    # Build network structure based on the model
    for i, l in enumerate(model.layers):
        layer = Layer(
            index=i,
            name=l.name,
            type=type(l).__name__,
            activation_function=l.activation.__name__,
            input_shape=l.input.shape,
            output_shape=l.output.shape,
            units=l.units,
        )

        for u in range(l.units):
            weights, biases = l.get_weights()
            neuron = Neuron(
                id=f"{layer.type}_{layer.index}_{neuron_counter}",
                layer_index=i,
                weight=weights[u], #TODO: np.ndarray and np.{type} shall be serializable
                bias=biases[u],
                activation_function=l.activation.__name__,
            )
            neuron_counter += 1
            layer.neurons.append(neuron)

        nn.add_layer(layer)
        print(layer)

    # TODO: incorrect works only with dense put if layers is Dence conditions
    # TODO: do same in one loop
    # Process connections between neurons
    for layer_index, layer in enumerate(model.layers):
        # if layer_index == 0:
        #     continue


        if hasattr(layer, 'weights'):
            weights = layer.get_weights()[0]
            biases = layer.get_weights()[1] if len(layer.get_weights()) > 1 else None

            prev_layer_neurons = nn.layers[layer_index - 1].neurons
            current_layer_neurons = nn.layers[layer_index].neurons

            for i, from_neuron in enumerate(prev_layer_neurons):
                for j, to_neuron in enumerate(current_layer_neurons):
                    weight = weights[i][j]
                    bias = float(biases[j]) if biases is not None else None
                    new_connection = Connection(
                        start=from_neuron.id,
                        end=to_neuron.id,
                        weight=float(weight),
                        bias=bias,
                    )
                    print(new_connection)
                    # nn.add_connection(new_connection)

    return nn
