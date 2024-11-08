import orjson
import numpy as np
from dataclasses import dataclass, asdict, is_dataclass, field
from typing import Any, Type, TypeVar, Union

T = TypeVar("T", bound="Serializable")


class Serializable:
    def to_json(self) -> str:
        """Serializes the dataclass to JSON."""
        return orjson.dumps(self, option=orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_INDENT_2, default=self._convert_numpy).decode()
    
    @classmethod
    def from_json(cls: Type[T], json_data: str) -> T:
        """Deserializes JSON data to recreate the dataclass structure."""
        data = orjson.loads(json_data)
        return cls._deserialize_data(cls, data)

    @classmethod
    def _deserialize_data(cls, target_cls: Type[T], data: dict) -> T:
        """Recursively reconstructs dataclass instances from dictionaries."""
        if not is_dataclass(target_cls):
            raise TypeError("from_json method can only be used with dataclass types")

        # Prepare the arguments dictionary for the target dataclass
        kwargs = {}
        for field in target_cls.__dataclass_fields__:
            field_type = target_cls.__dataclass_fields__[field].type
            field_value = data.get(field)

            # Handle nested dataclasses
            if is_dataclass(field_type) and isinstance(field_value, dict):
                kwargs[field] = cls._deserialize_data(field_type, field_value)
            # Handle lists of dataclasses (e.g., list[Neuron] in Layer)
            elif hasattr(field_type, "__origin__") and field_type.__origin__ == list:
                sub_type = field_type.__args__[0]
                if is_dataclass(sub_type) and isinstance(field_value, list):
                    kwargs[field] = [cls._deserialize_data(sub_type, item) for item in field_value]
                else:
                    kwargs[field] = field_value
            # Handle numpy types
            elif isinstance(field_value, float):
                kwargs[field] = np.float32(field_value)
            else:
                kwargs[field] = field_value

        return target_cls(**kwargs)

    @staticmethod
    def _convert_numpy(obj: Any):
        """Converts numpy objects to standard Python types for JSON serialization."""
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class ActivationFunction:
    pass


class LayerType:
    pass


@dataclass
class Neuron(Serializable):
    id: str
    layer_index: int
    weight: np.float32
    bias: float
    activation_function: Union[str, ActivationFunction] = None

    def to_dict(self):
        data = asdict(self)
        if self.activation_function is not None:
            data['activation_function'] = str(self.activation_function)
        return data


@dataclass
class Layer(Serializable):
    index: int
    type: Union[str, LayerType]
    name: str
    units: int
    input_shape: list[float]
    output_shape: list[float]
    activation_function: Union[str, ActivationFunction]
    neurons: list[Neuron] = field(default_factory=lambda: [])


@dataclass
class Connection(Serializable):
    start: str
    end: str
    weight: np.float32
    bias: float


@dataclass
class Topology(Serializable):
    layers: list[Layer] = field(default_factory=lambda: [])
    connections: list[Connection] = field(default_factory=lambda: [])

    def add_layer(self, layer: Layer):
        if layer in self.layers:
            raise ValueError("Layer already exists in layers")
        self.layers.append(layer)

    def add_connection(self, connection: Connection):
        if connection in self.connections:
            raise ValueError("Connection already exists in connections")
        self.connections.append(connection)