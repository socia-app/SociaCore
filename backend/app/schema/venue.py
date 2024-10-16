from typing import Optional
import uuid
from sqlmodel import SQLModel, Field
from app.models.venue import FoodcourtBase, NightclubBase, QSRBase, RestaurantBase

class VenueBase(SQLModel):
    name: str = Field(nullable=False)
    address: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    capacity: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default=None)
    google_rating: Optional[float] = Field(default=None)
    instagram_handle: Optional[str] = Field(default=None)
    instagram_token: Optional[str] = Field(default=None)
    google_map_link: Optional[str] = Field(default=None)
    mobile_number: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    opening_time: Optional[str] = Field(default=None)
    closing_time: Optional[str] = Field(default=None)
    avg_expense_for_two: Optional[float] = Field(default=None)
    qr_url: Optional[str] = Field(default=None)

class RestaurantRead(VenueBase):
    id: Optional[uuid.UUID]
    h3_index: Optional[str]
    class Config:
        from_attributes = True

class RestaurantCreate(VenueBase):
    class Config:
        from_attributes = True

class NightclubRead(VenueBase):
    id: Optional[uuid.UUID]
    h3_index: Optional[str]
    class Config:
        from_attributes = True

class NightclubCreate(VenueBase):
    class Config:
        from_attributes = True

class QSRRead(VenueBase):
    id: Optional[uuid.UUID]
    h3_index: Optional[str]
    class Config:
        from_attributes = True

class QSRCreate(VenueBase):
    class Config:
        from_attributes = True


class FoodcourtRead(FoodcourtBase):
    id: Optional[uuid.UUID]
    h3_index: Optional[str]
    class Config:
        from_attributes = True

class FoodcourtCreate(FoodcourtBase):
    class Config:
        from_attributes = True