from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Food(BaseModel):
    """Model from Bite 02"""

    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: Optional[float] = 0


app = FastAPI()
foods: Dict[int, Food] = {}


@app.post("/", status_code=201)
async def create_food(food: Food):
    """Endpoint from Bite 03"""
    foods[food.id] = food
    return food


@app.get("/", response_model=List[Food])
async def read_foods():
    """Endpoints from Bite 04"""
    return list(foods.values())


@app.get("/{food_id}", response_model=Food)
async def read_food(food_id: int):
    """Endpoints from Bite 04"""
    return foods[food_id]


# Create the update and delete endpoints here ...
@app.put('/{food_id}')
async def update_food(food_id: int, food: Food):
    if food_id not in foods:
        raise HTTPException(status_code=404, detail='Food not found')
    foods[food_id] = food
    return food


@app.delete('/{food_id}')
async def delete_food(food_id: int):
    if food_id not in foods:
        raise HTTPException(status_code=404, detail='Food not found')
    del foods[food_id]
    return {'ok': True}
