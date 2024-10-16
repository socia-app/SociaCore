from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import model_validator
import uuid
from datetime import datetime
from app.models.carousel_poster import CarouselPosterBase

class CarouselPosterCreate(CarouselPosterBase):
    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def validate_ids(cls, values):
        # values_dict = dict(values)
        ids = [values.get("event_id"), values.get("foodcourt_id"), values.get("nightclub_id"), values.get("restaurant_id"), values.get("qsr_id")]
        if sum(1 for id in ids if id is not None) != 1:
            raise ValueError("Exactly one of event_id, foodcourt_id, nightclub_id, restaurant_id, qsr_id must be present.")
        
        return values

class CarouselPosterRead(CarouselPosterBase):
    id: Optional[uuid.UUID]
    class Config:
        from_attributes = True
