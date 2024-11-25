from pymongo import MongoClient

client = MongoClient("mongodb://admin:password@mongodb:27017/")
db = client["db"]
documents = db["models"]

