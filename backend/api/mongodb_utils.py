from pymongo import MongoClient
import os

def get_db_connection():
    client = MongoClient(
        host=os.environ.get('DB_HOST', 'mongodb://localhost:27017'),
        username=os.environ.get('DB_USERNAME', ''),
        password=os.environ.get('DB_PASSWORD', '')
    )
    db = client[os.environ.get('DB_NAME', 'blog_db')]
    return db, client

# Usage example
# db, client = get_db_connection()
# collection = db['your_collection']
# result = collection.find({})
# client.close()  # close when done