import json
from core.src.convertor import convert
from sample.src.mnist import create_mnist_model
from core.src.models import Topology

# yes yes it's GPT generated
def verify_topology_structure(original_json: str, deserialized_topology: Topology) -> bool: 
    # Convert the deserialized topology back to JSON for direct comparison
    deserialized_json = deserialized_topology.to_json()
    
    # Compare JSON strings directly
    if original_json == deserialized_json:
        print("Direct JSON comparison passed: The structures are identical.")
        return True
    else:
        print("Direct JSON comparison failed: The structures differ.")
    
    # Convert JSON strings to dictionaries for a deeper comparison
    original_data = json.loads(original_json)
    deserialized_data = json.loads(deserialized_json)
    
    def deep_compare(d1, d2, path=""):
        """Recursively compare two dictionaries to find any differences."""
        if isinstance(d1, dict) and isinstance(d2, dict):
            for key in d1:
                if key not in d2:
                    print(f"Key '{path + key}' missing in deserialized data.")
                    return False
                if not deep_compare(d1[key], d2[key], path + key + "."):
                    return False
            for key in d2:
                if key not in d1:
                    print(f"Unexpected key '{path + key}' in deserialized data.")
                    return False
        elif isinstance(d1, list) and isinstance(d2, list):
            if len(d1) != len(d2):
                print(f"List length mismatch at '{path}'")
                return False
            for index, (item1, item2) in enumerate(zip(d1, d2)):
                if not deep_compare(item1, item2, f"{path}[{index}]."):
                    return False
        else:
            if d1 != d2:
                print(f"Mismatch at '{path}': {d1} != {d2}")
                return False
        return True
    
    # Run a deep comparison to identify any nested discrepancies
    if deep_compare(original_data, deserialized_data):
        print("Deep structure comparison passed: All nested structures match.")
        return True
    else:
        print("Deep structure comparison failed: Discrepancies found in nested structures.")
        return False

if __name__ == "__main__":
    model = create_mnist_model()
    topology = convert(model)

    topology_json = topology.to_json()
    with open("topology.json", "w") as file:
        file.write(topology_json)

    with open("topology.json", "r") as file:
        loaded_json = file.read()

    deserialized_topology = Topology.from_json(loaded_json)
    
    is_verified = verify_topology_structure(topology_json, deserialized_topology)
    print("Verification result:", "Passed" if is_verified else "Failed")