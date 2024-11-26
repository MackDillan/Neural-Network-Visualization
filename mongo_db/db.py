from pymongo import MongoClient

client = MongoClient("mongodb://admin:password@mongodb:27017/")
db = client["db"]
collection_models = db["models"]
collection_project = db["projects"]

