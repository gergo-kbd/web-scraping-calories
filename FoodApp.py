from OpenFoodApi.OpenFoodQuery import *
from OpenFoodApi.models import *
from usdaQuery.usda_food_query import *
from usdaQuery.models import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # vagy: ["*"] ha mindent engednél
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("api_key.txt", "r") as file:
        API_KEY = file.read().strip()

@app.get("/search_food")
def get_food(query:str):
    q = UsdaFoodQuery(API_KEY)
    data = q.search_food(query)
    parsed = FoodItem.from_dict(data['foods'])
    return parsed
    