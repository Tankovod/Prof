from pydantic import BaseModel, Field
from typing import Optional


class ProductValid(BaseModel):
    title: str = Field(default=..., min_length=3)
    description: Optional[str]
    amount: int = Field(default=..., gt=0)
    units: str = Field(default=...)
    image: Optional[str]
