from pydantic import BaseModel, Field, PositiveFloat
from typing import Optional


class ProductValid(BaseModel):
    title: str = Field(default=..., min_length=3)
    description: Optional[str]
    amount: PositiveFloat = Field(default=..., gt=0)
    units: str = Field(default=...)
    image: Optional[str]
