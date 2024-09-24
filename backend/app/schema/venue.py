from typing import Optional
from app.models.venue import FoodcourtBase, NightclubBase, QSRBase, RestaurantBase

class RestaurantRead(RestaurantBase):
    id: Optional[int]
    class Config:
        from_attributes = True

class RestaurantCreate(RestaurantBase):
    class Config:
        from_attributes = True

class NightclubRead(NightclubBase):
    id: Optional[int]
    class Config:
        from_attributes = True

class NightclubCreate(NightclubBase):
    class Config:
        from_attributes = True

class QSRRead(QSRBase):
    id: Optional[int]
    class Config:
        from_attributes = True

class QSRCreate(QSRBase):
    class Config:
        from_attributes = True


class FoodcourtRead(FoodcourtBase):
    id: Optional[int]
    class Config:
        from_attributes = True

class FoodcourtCreate(FoodcourtBase):
    class Config:
        from_attributes = True