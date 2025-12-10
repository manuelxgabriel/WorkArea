from fastapi import FastAPI
from fastapi.responses import FileResponse, Response, JSONResponse
from pathlib import Path
from pydantic import BaseModel
from database import database, user_collection

from pymongo import MongoClient
import certifi

app = FastAPI(title="FastAPI Microservice")
BASE_DIR = Path(__file__).resolve().parent
FAVICON_PATH = BASE_DIR / "static" / "favicon.ico"

# ---- Mongo Setup -----
# MONGO_URL = (
#     "mongodb+srv://manuelxgabriel:Elfuturo2021"
#     "@mservice-db.xyadzr7.mongodb.net/mservice-db"
#     "?appName=mservice-db"
# )
# client = MongoClient(
#     MONGO_URL,
#     serverSelectionTimeoutMS=2000,
#     tlsCAFile=certifi.where()
# )
# db = client.get_database()

foods = [
    {"name": "Pizza", "price": 12.43},
    {"name": "Sushi", "price": 31.83},
    {"name": "Pho", "price": 9.12}
]


class Item(BaseModel):
    name: str
    price: float


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    if FAVICON_PATH.exists():
        return FileResponse(BASE_DIR / "static" / "favicon.ico")
    return Response(status_code=204)


# -- Get Request --
@app.get("/")
async def read_root():
    return {"message": "Hello, from FASTAPI"}


@app.get("/items")
def get_item_list():
    return {"food-list": foods}


# -- Post Request --
@app.get("/items/")
def create_item(single_item: str):
    return {"message": f'You printed: {single_item}'}


# -- List All Users ---
@app.get("/users", response_description='List all users')
async def list_users():
    try:
        users_collection = database.get_collection('users')
        users = list(users_collection.find({}))

        for user in users:
            user['_id'] = str(user['_id'])

        return {"users": users}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# --- List All Collections ---
@app.get("/collections", response_description="List all collections")
async def list_collections():
    try:
        collections = database.list_collection_names()
        return {"collections": collections}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# -- Connection to MongoDB --
@app.get('/health')
def health_check():
    try:
        database.command("ping")
        print("MongoDB successfully connected!")
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "details": str(e)}
        )


# if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
