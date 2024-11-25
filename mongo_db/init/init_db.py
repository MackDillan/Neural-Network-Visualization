import json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://admin:password@mongodb:27017/")
db = client["db"]
collection = db["models"]
models_data = list()

for i in ['mnist', 'xor']:
    with open(f'/app/init/{i}.json', 'r') as file:
        models_data.append(json.load(file))

models = [
    {
        "_id": '2a033f59-4742-4d91-8eed-e2f03f7465a7',
        "latest_version": 1,
        "json_data": models_data[0],
        "created": datetime.utcnow(),
        "updated": datetime.utcnow()
    },
    {
        "_id": '2d4dd202-1863-4e6e-8541-7600c55ee078',
        "latest_version": 1,
        "json_data": models_data[1],
        "created": datetime.utcnow(),
        "updated": datetime.utcnow()
    }
]

try:
    collection.insert_many(models)
    print("Models inserted successfully!")
except Exception as e:
    print(f"Error occurred while")