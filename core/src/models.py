from dataclasses import dataclass, field

# TODO: need to hold lists of numbers as np.ndarray
# TODO: needs better way to serialize, mb have own Convertor json which can handle Serialization
# class Convertor:
#     def map(self, n: Neuron):
#         pass
#     def map(self, l: Layer):
#         pass
import orjson


class Serializable:
    def to_json(self):
        return orjson.dumps(self, option=orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_INDENT_2).decode()


class ActivationFunction:
    pass


class LayerType:
    pass


@dataclass
class Neuron(Serializable):
    id: str
    layer_index: int
    weight: list[float]
    bias: float
    activation_function: ActivationFunction = None


@dataclass
class Layer(Serializable):
    index: int
    type: LayerType
    name: str
    units: int
    input_shape: list[float]
    output_shape: list[float]
    activation_function: ActivationFunction
    neurons: list[Neuron] = field(default_factory=lambda: [])


@dataclass
class Connection(Serializable):
    start: str
    end: str
    weight: float
    bias: float


@dataclass
class Topology(Serializable):
    layers: list[Layer] = field(default_factory=lambda: [])
    connections: list[Connection] = field(default_factory=lambda: [])

    def add_layer(self, layer):
        if layer in self.layers:
            raise ValueError("Layer already exists in layers")
        self.layers.append(layer)

    def add_connection(self, connection):
        if connection in self.connections:
            raise ValueError("Connection already exists in connections")
        self.connections.append(connection)
