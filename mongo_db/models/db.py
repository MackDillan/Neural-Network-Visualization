from pymongo import MongoClient

client = MongoClient("mongodb://admin:password@mongodb:27017/")
db = client["db"]
models = db["models"]
#project = db["project"]

