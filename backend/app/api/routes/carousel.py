import uuid
import h3
from fastapi import APIRouter, Depends, Path
from sqlmodel import select
from typing import List
from app.models.carousel_poster import CarouselPoster
from app.models.venue import Nightclub, Restaurant, Foodcourt, QSR
from app.schema.carousel_poster import CarouselPosterCreate, CarouselPosterRead
from app.api.deps import SessionDep
from app.utils.h3_utils import get_h3_index, get_nearby_h3_indexes, fetch_h3_index
from app.utils.datetime import get_current_time
from app.utils.crud import create_record, delete_record, update_record

router = APIRouter()

@router.get("/poster/", response_model=List[CarouselPoster])
async def get_carousel_posters(
    latitude: float, longitude: float, session: SessionDep, radius: int = 3
):
    user_h3_index = get_h3_index(latitude=latitude, longitude=longitude)

    nearby_h3_indexes = get_nearby_h3_indexes(user_h3_index, radius)

    current_time = get_current_time()
    posters = (
        session.execute(
            select(CarouselPoster).where(CarouselPoster.h3_index.in_(nearby_h3_indexes))
            .where(CarouselPoster.expires_at > current_time)
        )
        .scalars()
        .all()
    )

    return posters

@router.post("/poster/", response_model=CarouselPosterRead)
async def create_carousel_poster(poster: CarouselPosterCreate, session: SessionDep):
    h3_index = None
    if poster.nightclub_id:
        h3_index = fetch_h3_index(session, Nightclub, poster.nightclub_id)
    elif poster.restaurant_id:
        h3_index = fetch_h3_index(session, Restaurant, poster.restaurant_id)
    elif poster.foodcourt_id:
        h3_index = fetch_h3_index(session, Foodcourt, poster.foodcourt_id)
    else:
        h3_index = fetch_h3_index(session, QSR, poster.qsr_id)

    carousel_poster_obj = CarouselPoster(**poster.model_dump(), h3_index=h3_index)

    return create_record(
        session=session, model=CarouselPoster, obj_in=carousel_poster_obj
    )


@router.put("/poster/{poster_id}", response_model=CarouselPosterRead)
async def update_carousel_poster(
    poster_id: uuid.UUID, updated_data: CarouselPosterCreate, session: SessionDep
):
    h3_index = None
    if updated_data.nightclub_id:
        h3_index = fetch_h3_index(session, Nightclub, updated_data.nightclub_id)
    elif updated_data.restaurant_id:
        h3_index = fetch_h3_index(session, Restaurant, updated_data.restaurant_id)
    elif updated_data.foodcourt_id:
        h3_index = fetch_h3_index(session, Foodcourt, updated_data.foodcourt_id)
    else:
        h3_index = fetch_h3_index(session, QSR, updated_data.qsr_id)

    carousel_poster_update_obj = CarouselPoster(**updated_data.model_dump(), h3_index=h3_index)
    
    return update_record(
        session=session, record_id=poster_id, obj_in=carousel_poster_update_obj, model=CarouselPoster
    )


@router.delete("/poster/{poster_id}")
async def delete_carousel_poster(poster_id: uuid.UUID, session: SessionDep):
    return delete_record(session=session, model=CarouselPoster, record_id=poster_id)
