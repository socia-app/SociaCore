from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import time

# Venue base details (composition)
class VenueCreate(BaseModel):
    name: str
    capacity: Optional[int] = None
    description: Optional[str] = None
    instagram_handle: Optional[str] = None
    instagram_token: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    avg_expense_for_two: Optional[float] = None
    zomato_link: Optional[str] = None
    swiggy_link: Optional[str] = None
    google_map_link : Optional[str] = None
    
class FoodcourtCreate(BaseModel):
    total_qsrs: Optional[int] = None
    seating_capacity: Optional[int] = None
    venue: VenueCreate
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
class QSRCreate(BaseModel):
    drive_thru: Optional[bool] = False
    foodcourt_id: Optional[uuid.UUID] = None
    venue: VenueCreate

class RestaurantCreate(VenueBase):
    class Config:
        from_attributes = True

# Restaurant Schemas
class RestaurantCreate(BaseModel):
    cuisine_type: Optional[str] = None
    venue_id: uuid.UUID
    venue: VenueCreate
class NightclubRead(VenueBase):
    id: Optional[uuid.UUID]
    h3_index: Optional[str]
    class Config:
        from_attributes = True


# Nightclub Schemas
class NightclubCreate(BaseModel):
    venue: VenueCreate
    age_limit: Optional[int] = None

class NightclubCreate(VenueBase):
    class Config:
        from_attributes = True


class VenueRead(BaseModel):
    id: uuid.UUID
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    capacity: Optional[int]
    description: Optional[str]
    google_rating: Optional[float]
    instagram_handle: Optional[str]
    google_map_link: Optional[str]
    mobile_number: Optional[str]
    email: Optional[str]
    opening_time: Optional[time]
    closing_time: Optional[time]
    avg_expense_for_two: Optional[float]
    zomato_link: Optional[str]
    swiggy_link: Optional[str]

class FoodcourtRead(BaseModel):
    id: uuid.UUID
    total_qsrs: Optional[int] = None  # Specific field for foodcourt
    seating_capacity: Optional[int] = None  # Specific to foodcourts
    venue: VenueRead
    qsrs: List["QSRRead"] = []  # List of QSRs in the foodcourt

class QSRRead(VenueBase):
    id: Optional[uuid.UUID]
    h3_index: Optional[str]
    class Config:
        from_attributes = True

class QSRRead(BaseModel):
    id: uuid.UUID
    # Add any specific fields for QSR if needed
    foodcourt_id: Optional[uuid.UUID] = None  # Reference to the associated foodcourt
    venue: VenueRead
class QSRCreate(VenueBase):
    class Config:
        from_attributes = True

class RestaurantRead(BaseModel):  
    id: uuid.UUID
    cuisine_type: Optional[str] = None
    venue: VenueRead

class FoodcourtRead(FoodcourtBase):
    id: Optional[uuid.UUID]
    h3_index: Optional[str]
    class Config:
        from_attributes = True

class NightclubRead(BaseModel):
    id: uuid.UUID
    age_limit: Optional[int] = None
    venue: VenueRead
    class Config:
        from_attributes = True
        
class VenueListResponse(BaseModel):
    nightclubs: List[NightclubRead]
    qsrs: List[QSRRead]   
    foodcourts: List[FoodcourtRead]
    restaurants: List[RestaurantRead]