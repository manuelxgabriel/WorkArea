from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from pathlib import Path

app = FastAPI(title="FastAPI Microservice")
BASE_DIR = Path(__file__).resolve().parent
FAVICON_PATH = BASE_DIR / "static" / "favicon.ico"

foods = [
    "Pizza",
    "Sushi",
    "Hamburger",
    "Pasta",
    "Salad",
    "Tacos",
    "Steak",
    "Fried Rice",
    "Ramen",
    "Curry",
    "Sandwich",
    "Burrito",
    "Dumplings",
    "Ice Cream",
    "Chocolate",
    "Pancakes",
    "Hot Dog",
    "Falafel",
    "Paella",
    "Pho"
]


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    if FAVICON_PATH.exists():
        return FileResponse(BASE_DIR / "static" / "favicon.ico")
    return Response(status_code=204)


# -- Get Request --
@app.get("/")
async def read_root():
    return {"message": "Hello, from FASTAPI"}


@app.get("/food-items")
def get_item_list():
    return {"food-list": foods}

# -- Post Request --


