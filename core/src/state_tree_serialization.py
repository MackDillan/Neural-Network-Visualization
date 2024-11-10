import json
import tensorflow as tf
import numpy as np

def serialize_variable(obj):
    if isinstance(obj, tf.Variable):
        return {
            "__type__": "tf.Variable",
            "name": obj.name,
            "dtype": str(obj.dtype.name),
            "shape": obj.shape.as_list(),
            "data": serialize_variable(obj.numpy())
        }
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return {
            "__type__": "np.floating",
            "dtype": str(obj.dtype),
            "data": float(obj)
        }
    elif isinstance(obj, np.ndarray):
        return {
            "__type__": "ndarray",
            "dtype": str(obj.dtype),
            "shape": obj.shape,
            "data": obj.tolist()
        }
    elif isinstance(obj, np.integer):
        return {
            "__type__": "np.integer",
            "dtype": str(obj.dtype),
            "data": int(obj)
        }
    elif isinstance(obj, (np.bool_, bool)):
        return {
            "__type__": "np.bool_" if isinstance(obj, np.bool_) else "bool",
            "data": bool(obj)
        }
    elif isinstance(obj, (np.complexfloating, complex)):
        return {
            "__type__": "complex",
            "dtype": str(obj.dtype) if hasattr(obj, 'dtype') else "complex",
            "data": [obj.real, obj.imag]
        }
    else:
        raise TypeError(f"Type {type(obj)} not supported for serialization")


def deserialize_variable(data):
    if data is None:
        return None

    if isinstance(data, dict):
        obj_type = data.get("__type__")
        
        if obj_type == "tf.Variable":
            dtype_str = data["dtype"]
            dtype = tf.as_dtype(dtype_str) if dtype_str else None
            return tf.Variable(
                initial_value=deserialize_variable(data["data"]),
                dtype=dtype,
                name=data["name"],
                trainable=False
            )
        
        elif obj_type == "np.floating":
            dtype = np.dtype(data["dtype"])
            return np.array(data["data"], dtype=dtype).item()
        
        elif obj_type == "ndarray":
            dtype = np.dtype(data["dtype"])
            return np.array(data["data"], dtype=dtype).reshape(data["shape"])
        
        elif obj_type == "np.integer":
            dtype = np.dtype(data["dtype"])
            return np.array(data["data"], dtype=dtype).item()
        
        elif obj_type in ("np.bool_", "bool"):
            return bool(data["data"])
        
        elif obj_type == "complex":
            return complex(data["data"][0], data["data"][1])
        
        else:
            return {key: deserialize_variable(value) for key, value in data.items()}

    elif isinstance(data, list):
        return [deserialize_variable(item) for item in data]

    else:
        return data


def serialize_state_tree(state_tree):
    if isinstance(state_tree, dict):
        return {key: serialize_state_tree(value) for key, value in state_tree.items()}
    return serialize_variable(state_tree)


def save_state_tree_to_json(model, file_path="state_tree.json"):
    state_tree = model.get_state_tree()
    serialized_state_tree = serialize_state_tree(state_tree)
    
    with open(file_path, "w") as file:
        json.dump(serialized_state_tree, file, indent=4)
    
    return serialized_state_tree


def load_state_tree_from_json(file_path="state_tree.json"):
    with open(file_path, "r") as file:
        loaded_data = json.load(file)
    return deserialize_variable(loaded_data)


#verification
def compare_state_trees(tree1, tree2):
    if isinstance(tree1, dict) and isinstance(tree2, dict):
        if tree1.keys() != tree2.keys():
            print("Difference in keys:", tree1.keys(), tree2.keys())
            return False
        return all(compare_state_trees(tree1[key], tree2[key]) for key in tree1)

    elif isinstance(tree1, list) and isinstance(tree2, list):
        if len(tree1) != len(tree2):
            print("Difference in list lengths:", len(tree1), len(tree2))
            return False
        return all(compare_state_trees(item1, item2) for item1, item2 in zip(tree1, tree2))

    elif isinstance(tree1, tf.Variable) and isinstance(tree2, tf.Variable):
        if tree1.dtype != tree2.dtype:
            print("Difference in variable dtype:", tree1.dtype, tree2.dtype)
            return False
        if tree1.shape != tree2.shape:
            print("Difference in variable shape:", tree1.shape, tree2.shape)
            return False
        if not np.allclose(tree1.numpy(), tree2.numpy()):
            print("Difference in variable values:", tree1.numpy(), tree2.numpy())
            return False
        if tree1.name.split(":")[0] != tree2.name.split(":")[0]:
            print("Difference in variable names:", tree1.name, tree2.name)
            return False
        return True

    else:
        if tree1 != tree2:
            print("Difference in values:", tree1, tree2)
            return False
        return True
