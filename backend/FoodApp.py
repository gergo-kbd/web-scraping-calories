import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from OpenFoodApi.OpenFoodQuery import *
from OpenFoodApi.models import *
from usdaQuery.usda_food_query import *
from usdaQuery.models import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
api_key_path = os.path.join(project_root, "api_key.txt")

try:
    with open(api_key_path, "r") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    print("APIKEY cannot be found.")
except Exception as e:
    print("ERROR occured during file read.")

@app.get("/search_food")
def get_food(query:str):
    q = UsdaFoodQuery(API_KEY)
    data = q.search_food(query)
    parsed = FoodItem.from_dict(data['foods'])
    return parsed
    