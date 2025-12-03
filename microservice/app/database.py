from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values
import certifi
import os

load_dotenv(dotenv_path=".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
print(DB_USER, DB_PASSWORD)


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

user_collection = database.get_collection('users')
