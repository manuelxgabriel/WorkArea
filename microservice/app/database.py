from pymongo import MongoClient
import certifi
import os

DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")

MONGO_URL = (

    f'mongodb+srv://{DB_USER}:{DB_PASSWORD}'
    '@mservice-db.xyadzr7.mongodb.net/mservice-db'
    '?appName=mservice-db'
)

client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=2000,
    tlsCAFile=certifi.where()
)

database = client.get_database()

# user_collection = database.get_collection('users')
