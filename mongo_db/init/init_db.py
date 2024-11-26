import json
from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient("mongodb://admin:password@mongodb:27017/")
db = client["db"]
models_collection = db["models"]
projects_collection = db["projects"]
models_data = list()

for i in ['mnist', 'xor']:
    with open(f'/app/init/{i}.json', 'r') as file:
        models_data.append(json.load(file))

models = [
    {
        "_id": '2a033f59-4742-4d91-8eed-e2f03f7465a7',
        "latest_version": 1,
        "json_data": models_data[0],
        "created": datetime.now(timezone.utc),
        "updated": datetime.now(timezone.utc)
    },
    {
        "_id": '2d4dd202-1863-4e6e-8541-7600c55ee078',
        "latest_version": 1,
        "json_data": models_data[1],
        "created": datetime.now(timezone.utc),
        "updated": datetime.now(timezone.utc)
    }
]

projects = [
    {    
        '_id': '2d4dd202-1863-4e6e-8541-7600c55ee078',
        'name': 'MNIST NN',
        'model_link': '2a033f59-4742-4d91-8eed-e2f03f7465a7',
        'dataset_name': 'MNIST',
        'description': 'MNIST NN',
        "created": datetime.now(timezone.utc),
        "updated": datetime.now(timezone.utc)
    },
    {    
        '_id': '2a033f59-4742-4d91-8eed-e2f03f7465a7',
        'name': 'XOR NN',
        'model_link': '2a033f59-4742-4d91-8eed-e2f03f7465a7',
        'dataset_name': 'XOR',
        'description': 'XOR NN',
        "created": datetime.now(timezone.utc),
        "updated": datetime.now(timezone.utc)
    },

]

try:
    models_collection.insert_many(models)
    print("Models inserted successfully!")
except Exception as e:
    print(f"Error occurred while")

try:
    projects_collection.insert_many(projects)
    print("Projects inserted successfully!")
except Exception as e:
    print(f"Error occurred while")