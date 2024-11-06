import json
from tensorflow.keras.models import load_model 

# Class representing an individual neuron
class Neuron:
    """
    Represents an individual neuron in a neural network.

    Attributes:
        neuron_id (str): Unique identifier for the neuron.
        layer_index (int): Index of the layer the neuron belongs to.
        activation_function (str, optional): Activation function of the neuron, if specified.
    """
    def __init__(self, neuron_id, layer_index, activation_function=None):
        self.neuron_id = neuron_id
        self.layer_index = layer_index
        self.activation_function = activation_function

# Class representing a layer
class Layer:
    """
    Represents a layer in a neural network.

    Attributes:
        layer_index (int): Index of the layer within the network.
        layer_type (str): Type of the layer (e.g., Dense, Flatten, Conv2D).
        activation_function (str, optional): Activation function of the layer, if specified.
        neurons (list): List of neurons in this layer.
    """
    def __init__(self, layer_index, layer_type, activation_function=None):
        self.layer_index = layer_index
        self.layer_type = layer_type
        self.activation_function = activation_function
        self.neurons = []

    def add_neuron(self, neuron):
        self.neurons.append(neuron)

# Class representing a connection between neurons
class Connection:
    """
    Represents a connection between two neurons in the neural network.

    Attributes:
        from_neuron (str): Source neuron ID.
        to_neuron (str): Destination neuron ID.
        weight (float): Weight of the connection.
        bias (float, optional): Bias of the connection, if available.
    """
    def __init__(self, from_neuron, to_neuron, weight, bias=None):
        self.from_neuron = from_neuron
        self.to_neuron = to_neuron
        self.weight = weight
        self.bias = bias

# Class representing the entire neural network
class NeuralNetwork:
    """
    Represents the entire neural network structure.

    Attributes:
        layers (list): List of layers in the network.
        connections (list): List of all connections between neurons in the network.
    """
    def __init__(self):
        self.layers = []
        self.connections = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def add_connection(self, connection):
        self.connections.append(connection)

model = load_model("my_model.keras")

# Create an object representing the neural network
nn = NeuralNetwork()
neuron_counter = 0  # Counter for unique neuron identifiers
neuron_ids = {}  # Dictionary for storing neuron ID mappings

# Build network structure based on the model
for layer_index, layer in enumerate(model.layers):
    layer_type = type(layer).__name__
    activation_function = layer.activation.__name__ if hasattr(layer, 'activation') else None
    new_layer = Layer(layer_index=layer_index, layer_type=layer_type, activation_function=activation_function)

    num_neurons = layer.units if hasattr(layer, 'units') else int(layer.output.shape[1])
    for i in range(num_neurons):
        neuron_id = f"{layer_type}_{layer_index}_{neuron_counter}"
        neuron_counter += 1
        new_neuron = Neuron(neuron_id=neuron_id, layer_index=layer_index, activation_function=activation_function)
        new_layer.add_neuron(new_neuron)
        neuron_ids[(layer_index, i)] = new_neuron

    nn.add_layer(new_layer)

# Process connections between neurons
for layer_index, layer in enumerate(model.layers):
    if layer_index == 0:
        continue

    if hasattr(layer, 'weights'):
        weights = layer.get_weights()[0]
        biases = layer.get_weights()[1] if len(layer.get_weights()) > 1 else None

        prev_layer_neurons = nn.layers[layer_index - 1].neurons
        current_layer_neurons = nn.layers[layer_index].neurons

        for i, from_neuron in enumerate(prev_layer_neurons):
            for j, to_neuron in enumerate(current_layer_neurons):
                weight = weights[i][j]
                bias = float(biases[j]) if biases is not None else None
                new_connection = Connection(from_neuron=from_neuron.neuron_id, to_neuron=to_neuron.neuron_id, weight=float(weight), bias=bias)
                nn.add_connection(new_connection)

# Convert network structure to JSON-compatible format
nn_structure = {
    "layers": [],
    "neurons": [],
    "connections": []
}

# Convert layers to JSON-compatible format
for layer in nn.layers:
    layer_info = {
        "layer_index": layer.layer_index,
        "layer_type": layer.layer_type,
        "num_neurons": len(layer.neurons),
        "activation_function": layer.activation_function,
        "neurons": [neuron.neuron_id for neuron in layer.neurons]
    }
    nn_structure["layers"].append(layer_info)

# Convert neurons to JSON-compatible format
for layer in nn.layers:
    for neuron in layer.neurons:
        neuron_info = {
            "neuron_id": neuron.neuron_id,
            "layer_index": neuron.layer_index,
            "activation_function": neuron.activation_function
        }
        nn_structure["neurons"].append(neuron_info)

# Convert connections to JSON-compatible format
for connection in nn.connections:
    connection_info = {
        "from_neuron": connection.from_neuron,
        "to_neuron": connection.to_neuron,
        "weight": connection.weight,
        "bias": connection.bias
    }
    nn_structure["connections"].append(connection_info)

# Save the neural network structure to a JSON file
with open("neural_network_structure.json", "w") as json_file:
    json.dump(nn_structure, json_file, indent=4)

print("Neural network structure information saved to 'neural_network_structure.json'")
