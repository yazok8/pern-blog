from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['breakloose'] 

# You can add helper functions here
def get_collection(collection_name):
    return db[collection_name]
