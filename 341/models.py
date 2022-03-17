from datetime import datetime
from typing import Any, Optional

from passlib.context import CryptContext
from pydantic import BaseModel

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# which we'll further explore in a later Bite
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class Food(BaseModel):
    """Bite 02"""

    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: Optional[float] = 0


# Write the User and FoodEntry models here ...
class User(BaseModel):
    id: int
    username: str
    password: str

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.password = get_password_hash(data['password'])


class FoodEntry(BaseModel):
    id: int
    user: User
    food: Food
    date_added: datetime = datetime.now()
    number_servings: float

    @property
    def total_calories(self):
        return self.number_servings * self.food.kcal_per_serving
