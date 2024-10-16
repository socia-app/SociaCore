from typing import List
from app.models.user import UserBusiness, UserVenueAssociation
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session
from app.models.venue import QSR, Foodcourt, Restaurant, Nightclub, Venue
from app.schema.venue import (
    FoodcourtCreate,
    QSRCreate,
    RestaurantCreate,
    NightclubCreate,
    FoodcourtRead,
    QSRRead,
    RestaurantRead,
    NightclubRead,
    VenueListResponse,
)
from app.api.deps import get_business_user, get_db  # Assuming you have a dependency to get the database session
from app.util import (
    create_record,
import uuid
from app.schema.venue import FoodcourtCreate, FoodcourtRead, NightclubCreate, NightclubRead, QSRCreate, QSRRead, RestaurantCreate, RestaurantRead
from app.models.user import UserBusiness, UserPublic
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Union
from app.utils import get_h3_index

from app.models.venue import Nightclub, Restaurant, QSR, Foodcourt
from app.api.deps import SessionDep, get_business_user, get_current_user, get_super_user
from app.crud import (
    get_all_records,
)

app = FastAPI()
router = APIRouter()

# POST endpoint for Foodcourt
@router.post("/foodcourts/", response_model=FoodcourtRead)
def create_foodcourt(foodcourt: FoodcourtCreate, db: Session = Depends(get_db),
                current_user: UserBusiness = Depends(get_business_user)):
    try:
        # Check if the venue exists
        venue_instance = Venue.from_create_schema(foodcourt.venue)
        create_record(db, venue_instance)  # Persist the new venue
        # Use the newly created venue instance
        foodcourt_instance = Foodcourt.from_create_schema(venue_instance.id, foodcourt)
        # Create the new Foodcourt record in the database
        create_record(db, foodcourt_instance)
        association = UserVenueAssociation(
            user_id=current_user.id,
            venue_id=venue_instance.id
        )
        create_record(db, association)
        
        return foodcourt_instance.to_read_schema()
    
    except Exception as e:
        # Rollback the session in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Respond with a 500 error

# GET endpoint for Foodcourt
@router.get("/foodcourts/", response_model=List[FoodcourtRead])
def read_foodcourts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_records(db, Foodcourt, skip=skip, limit=limit)

# POST endpoint for QSR
@router.post("/qsrs/", response_model=QSRRead)
def create_qsr(qsr: QSRCreate, db: Session = Depends(get_db),
               current_user: UserBusiness = Depends(get_business_user)):
    try:
        # Check if the venue exists
        venue_instance = Venue.from_create_schema(qsr.venue)
        create_record(db, venue_instance)  # Persist the new venue
        # Use the newly created venue instance
        qsr_instance = QSR.from_create_schema(venue_instance.id, qsr)
        # Create the new Foodcourt record in the database
        create_record(db, qsr_instance)
        association = UserVenueAssociation(
            user_id=current_user.id,
            venue_id=venue_instance.id
        )
        create_record(db, association)
        return qsr_instance.to_read_schema()
    
    except Exception as e:
        # Rollback the session in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Respond with a 500 error

# GET endpoint for QSR
@router.get("/qsrs/", response_model=List[QSRRead])
def read_qsrs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_records(db, QSR, skip=skip, limit=limit)

# POST endpoint for Restaurant
@router.post("/restaurants/", response_model=RestaurantRead)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db),
                      current_user: UserBusiness = Depends(get_business_user)):
    try:
        # Check if the venue exists
        venue_instance = Venue.from_create_schema(restaurant.venue)
        create_record(db, venue_instance)  # Persist the new venue
        # Use the newly created venue instance
        restaurant_instance = Restaurant.from_create_schema(venue_instance.id, restaurant)
        # Create the new Foodcourt record in the database
        create_record(db, restaurant_instance)
        association = UserVenueAssociation(
            user_id=current_user.id,
            venue_id=venue_instance.id
        )
        create_record(db, association)
        return restaurant_instance.to_read_schema()
    
    except Exception as e:
        # Rollback the session in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Respond with a 500 error

# GET endpoint for Restaurant
# CRUD operations for Nightclubs

@router.get("/nightclubs/", response_model=List[NightclubRead])
async def read_nightclubs(
    session: SessionDep,
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100),
    current_user: Union[UserPublic, UserBusiness] = Depends(get_current_user)
):
    """
    Retrieve a paginated list of nightclubs.
    - **skip**: The page number (starting from 0)
    - **limit**: The number of items per page
    """
    nightclubs = get_all_records(session, Nightclub, skip=skip, limit=limit)
    return nightclubs 

@router.get("/nightclubs/{venue_id}", response_model=NightclubRead)
async def read_nightclub(
    venue_id: uuid.UUID, session: SessionDep, 
    current_user: Union[UserPublic, UserBusiness] = Depends(get_current_user)
):
    nightclub = get_record_by_id(session, Nightclub, venue_id)
    if not nightclub:
        raise HTTPException(status_code=404, detail="Nightclub not found")
    return nightclub

@router.post("/nightclubs/", response_model=NightclubRead)
async def create_nightclub(
    nightclub: NightclubCreate,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_business_user)
):
    venue_h3_index = get_h3_index(latitude=nightclub.latitude, longitude=nightclub.longitude)
    nightclub_obj = Nightclub(**nightclub.model_dump(), h3_index=venue_h3_index)

    return create_record(session, Nightclub, nightclub_obj)

@router.put("/nightclubs/{venue_id}", response_model=Nightclub)
async def update_nightclub(
    venue_id: uuid.UUID,
    updated_nightclub: NightclubCreate,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_business_user)
    ):
    venue_h3_index = get_h3_index(latitude=updated_nightclub.latitude, longitude=updated_nightclub.longitude)
    updated_nightclub = Nightclub(**updated_nightclub.model_dump(), h3_index=venue_h3_index)
    return update_record(session, Nightclub, venue_id, updated_nightclub)

@router.delete("/nightclubs/{venue_id}", response_model=None)
async def delete_nightclub(
    venue_id: uuid.UUID,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_super_user)
):
    return delete_record(session, Nightclub, venue_id)

@router.get("/restaurants/", response_model=List[RestaurantRead])
def read_restaurants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_records(db, Restaurant, skip=skip, limit=limit)

# POST endpoint for Nightclub
@router.post("/nightclubs/", response_model=NightclubRead)
def create_nightclub(nightclub: NightclubCreate, db: Session = Depends(get_db),
                     current_user: UserBusiness = Depends(get_business_user)):
    try:
        # Check if the venue exists
        venue_instance = Venue.from_create_schema(nightclub.venue)
        create_record(db, venue_instance)  # Persist the new venue
        # Use the newly created venue instance
        nightclub_instance = Nightclub.from_create_schema(venue_instance.id, nightclub)
        # Create the new Foodcourt record in the database
        create_record(db, nightclub_instance)
        association = UserVenueAssociation(
            user_id=current_user.id,
            venue_id=venue_instance.id
        )
        create_record(db, association)
        return nightclub_instance.to_read_schema()
    
    except Exception as e:
        # Rollback the session in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Respond with a 500 error

# GET endpoint for Nightclub
@router.get("/nightclubs/", response_model=List[NightclubRead])
def read_nightclubs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_records(db, Nightclub, skip=skip, limit=limit)

@router.get("/my-venues/", response_model=VenueListResponse)
async def get_my_venues(
    db: Session = Depends(get_db),
    current_user: UserBusiness = Depends(get_business_user)
):
    venue_h3_index = get_h3_index(latitude=restaurant.latitude, longitude=restaurant.longitude)
    restaurant = Restaurant(**restaurant.model_dump(), h3_index=venue_h3_index)

    return create_record(session, Restaurant, restaurant)

@router.put("/restaurants/{venue_id}", response_model=Restaurant)
async def update_restaurant(
    venue_id: uuid.UUID,
    updated_restaurant: RestaurantCreate,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_business_user)
    ):
    venue_h3_index = get_h3_index(latitude=updated_restaurant.latitude, longitude=updated_restaurant.longitude)
    updated_restaurant = Restaurant(**updated_restaurant.model_dump(), h3_index=venue_h3_index)
    return update_record(session, Restaurant, venue_id, updated_restaurant)

@router.delete("/restaurants/{venue_id}", response_model=None)
async def delete_restaurant(
    venue_id: uuid.UUID,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_super_user)
):
    return delete_record(session, Restaurant, venue_id)

@router.get("/qsrs/", response_model=List[QSRRead])
async def read_qsrs(
    session: SessionDep,
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100),
    current_user: Union[UserPublic, UserBusiness] = Depends(get_current_user)
):
    """
    Retrieve the venues managed by the current user, organized by venue type.
    
    This method leverages SQLAlchemy's efficient querying capabilities to minimize database load
    while ensuring data integrity through the association table, UserVenueAssociation.
    """

    # Fetch all venues managed by the current user
    managed_venues = (
        db.query(Venue)
        .join(UserVenueAssociation)
        .filter(UserVenueAssociation.user_id == current_user.id)
        .all()
    )

    # Create a set for fast membership testing
    managed_venue_ids = {venue.id for venue in managed_venues}

    # Initialize lists for categorized venues
    nightclubs, qsrs, foodcourts, restaurants = [], [], [], []

    # Efficiently query and convert Nightclubs
    for nightclub in db.query(Nightclub).filter(Nightclub.venue_id.in_(managed_venue_ids)).all():
        nightclubs.append(nightclub.to_read_schema())

    # Efficiently query and convert QSRs
    for qsr in db.query(QSR).filter(QSR.venue_id.in_(managed_venue_ids)).all():
        qsrs.append(qsr.to_read_schema())

    # Efficiently query and convert Foodcourts
    for foodcourt in db.query(Foodcourt).filter(Foodcourt.venue_id.in_(managed_venue_ids)).all():
        foodcourts.append(foodcourt.to_read_schema())

    # Efficiently query and convert Restaurants
    for restaurant in db.query(Restaurant).filter(Restaurant.venue_id.in_(managed_venue_ids)).all():
        restaurants.append(restaurant.to_read_schema())

    # Construct and return the response
    return VenueListResponse(
        nightclubs=nightclubs,
        qsrs=qsrs,
        foodcourts=foodcourts,
        restaurants=restaurants
    )
    Retrieve a paginated list of qsrs.
    - **skip**: The page number (starting from 0)
    - **limit**: The number of items per page
    """
    qsrs = get_all_records(session, QSR, skip=skip, limit=limit)
    return qsrs 

@router.get("/qsrs/{venue_id}", response_model=QSRRead)
async def read_qsr(
    venue_id: uuid.UUID, session: SessionDep ,
    current_user: Union[UserPublic, UserBusiness] = Depends(get_current_user)):
    qsr = get_record_by_id(session, QSR, venue_id)
    if not qsr:
        raise HTTPException(status_code=404, detail="QSR not found")
    return qsr

@router.post("/qsrs/", response_model=QSRRead)
async def create_qsr(
    qsr: QSRCreate,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_business_user)
):
    venue_h3_index = get_h3_index(latitude=qsr.latitude, longitude=qsr.longitude)
    qsr = QSR(**qsr.model_dump(), h3_index=venue_h3_index)
    return create_record(session, QSR, qsr)

@router.put("/qsrs/{venue_id}", response_model=QSR)
async def update_qsr(
    venue_id: uuid.UUID,
    updated_qsr: QSRCreate,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_business_user)
    ):
    venue_h3_index = get_h3_index(latitude=updated_qsr.latitude, longitude=updated_qsr.longitude)
    updated_qsr = QSR(**updated_qsr.model_dump(), h3_index=venue_h3_index)
    return update_record(session, QSR, venue_id, updated_qsr)

@router.delete("/qsrs/{venue_id}", response_model=None)
async def delete_qsr(
    venue_id: uuid.UUID,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_super_user)
):
    return delete_record(session, QSR, venue_id)

@router.get("/foodcourts/", response_model=List[FoodcourtRead])
async def read_foodcourts(
    session: SessionDep,
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100),
    current_user: Union[UserPublic, UserBusiness] = Depends(get_current_user)
):
    """
    Retrieve a paginated list of foodcourts.
    - **skip**: The page number (starting from 0)
    - **limit**: The number of items per page
    """
    foodcourts = get_all_records(session, Foodcourt, skip=skip, limit=limit)
    return foodcourts 

@router.get("/foodcourts/{venue_id}", response_model=FoodcourtRead)
async def read_foodcourt(
    venue_id: uuid.UUID, session: SessionDep ,
    current_user: Union[UserPublic, UserBusiness] = Depends(get_current_user)):
    foodcourt = get_record_by_id(session, Foodcourt, venue_id)
    if not foodcourt:
        raise HTTPException(status_code=404, detail="foodcourt not found")
    return foodcourt

@router.post("/foodcourts/", response_model=FoodcourtRead)
async def create_foodcourt(
    foodcourt: FoodcourtCreate,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_business_user)
):
    venue_h3_index = get_h3_index(latitude=foodcourt.latitude, longitude=foodcourt.longitude)
    foodcourt = Foodcourt(**foodcourt.model_dump(), h3_index=venue_h3_index)
    return create_record(session, Foodcourt, foodcourt)

@router.put("/foodcourts/{venue_id}", response_model=Foodcourt)
async def update_foodcourt(
    venue_id: uuid.UUID,
    updated_foodcourt: FoodcourtCreate,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_business_user),
    ):
    venue_h3_index = get_h3_index(latitude=updated_foodcourt.latitude, longitude=updated_foodcourt.longitude)
    updated_foodcourt = Foodcourt(**updated_foodcourt.model_dump(), h3_index=venue_h3_index)
    return update_record(session, Foodcourt, venue_id, updated_foodcourt)

@router.delete("/foodcourts/{venue_id}", response_model=None)
async def delete_foodcourt(
    venue_id: uuid.UUID,
    session: SessionDep,
    current_user: UserBusiness = Depends(get_super_user)
    
):
    return delete_record(session, Foodcourt, venue_id)