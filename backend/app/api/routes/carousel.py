import uuid
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlmodel import select, Session
from typing import List
from app.models.user import UserBusiness
from app.models.carousel_poster import CarouselPoster
from app.schema.carousel_poster import CarouselPosterCreate, CarouselPosterRead
from app.api.deps import get_business_user, get_db
from app.utils.h3_utils import get_h3_index, get_nearby_h3_indexes, fetch_h3_index
from app.utils.datetime import get_current_time
from app.utils.crud import create_record, delete_record, update_record, get_record_by_id

router = APIRouter()

@router.get("/poster/", response_model=List[CarouselPoster])
async def get_carousel_posters(
    latitude: float, longitude: float, radius: int = 3, db: Session = Depends(get_db)
):
    try:
        user_h3_index = get_h3_index(latitude=latitude, longitude=longitude)

        nearby_h3_indexes = get_nearby_h3_indexes(user_h3_index, radius)

        current_time = get_current_time()
        posters = (
            db.execute(
                select(CarouselPoster)
                .where(CarouselPoster.h3_index.in_(nearby_h3_indexes))
                .where(CarouselPoster.expires_at > current_time)
            )
            .scalars()
            .all()
        )

        return posters

    except Exception as e:
        # Rollback the session in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Respond with a 500 error


@router.post("/poster/", response_model=CarouselPosterRead)
async def create_carousel_poster(
    poster: CarouselPosterCreate,
    db: Session = Depends(get_db),
    # current_user: UserBusiness = Depends(get_business_user),
):
    try:

        carousel_poster_obj = CarouselPoster.from_create_schema(db, poster)
        created_carousel_poster = create_record(db, carousel_poster_obj)

        return CarouselPoster.to_read_schema(created_carousel_poster)
    except Exception as e:
        # Rollback the session in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Respond with a 500 error


@router.put("/poster/{poster_id}", response_model=CarouselPosterRead)
async def update_carousel_poster(
    poster_id: uuid.UUID,
    poster: CarouselPosterCreate,
    db: Session = Depends(get_db),
    current_user: UserBusiness = Depends(get_business_user),
):
    try:
        carousel_poster_instance = get_record_by_id(db, CarouselPoster, poster_id)
        if not carousel_poster_instance:
            raise HTTPException(status_code=404, detail="Carousel poster not found.")

        carousel_poster_update_obj = CarouselPoster.from_create_schema(db, poster)

        updated_carousel_poster = update_record(
            db, carousel_poster_instance, carousel_poster_update_obj
        )

        return CarouselPoster.to_read_schema(updated_carousel_poster)

    except Exception as e:
        # Rollback the session in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/poster/{poster_id}")
async def delete_carousel_poster(poster_id: uuid.UUID, db: Session = Depends(get_db)):
    carousel_poster = get_record_by_id(db, CarouselPoster, poster_id)
    if not carousel_poster:
        raise HTTPException(status_code=404, detail="Carousel poster not found.")
    
    return delete_record(db, carousel_poster)
