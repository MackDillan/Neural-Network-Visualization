import keras
from core.src.models import Topology, Layer, Neuron, Connection


def convert(model: keras.Sequential) -> Topology:
    nn = Topology()
    # Build network structure based on the model
    for layer_index, l in enumerate(model.layers):
        neuron_counter = 0  # Counter for unique neuron identifiers
        model_type = type(l).__name__
        layer = Layer(
            index=layer_index,
            name=l.name,
            type=model_type,
            activation_function=l.activation.__name__ if hasattr(l, 'activation') else None,
            input_shape=l.input.shape,
            output_shape=l.output.shape,
            units=l.units if hasattr(l, 'units') else None,
        )

        if model_type == 'Flatten':
            continue

        for u in range(l.units):
            weights, biases = l.get_weights()
            neuron = Neuron(
                id=f"{layer.type}_{layer.index}_{neuron_counter}",
                layer_index=layer_index,
                weight=weights[u],
                bias=biases[u],
                activation_function=l.activation.__name__,
            )
            layer.neurons.append(neuron)
        
            if hasattr(l, 'weights') and layer_index >= 2:
                prev_layer_neurons = nn.layers[layer_index - 2].neurons
                for from_neuron_index, from_neuron in enumerate(prev_layer_neurons):
                    weight = weights[from_neuron_index][neuron_counter]
                    bias = float(biases[neuron_counter]) if biases is not None else None
                    new_connection = Connection(
                        start=from_neuron.id,
                        end=neuron.id,
                        weight=float(weight),
                        bias=bias,
                    )

                    #print(new_connection)
                    nn.add_connection(new_connection)
            neuron_counter += 1

        nn.add_layer(layer)
    return nn
