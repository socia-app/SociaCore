import uuid
from sqlmodel import SQLModel, Field, Relationship, Session
from app.schema.carousel_poster import CarouselPosterCreate, CarouselPosterRead
from app.models.venue import Nightclub, Restaurant, Foodcourt, QSR
from app.utils.h3_utils import fetch_h3_index
from typing import Optional
from datetime import datetime

class CarouselPosterBase(SQLModel):
    image_url: str = Field(nullable=False)
    deep_link: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    
    # Foreign keys [Optional]
    event_id: Optional[uuid.UUID] = Field(default=None, foreign_key="event.id")
    nightclub_id: Optional[uuid.UUID] = Field(default=None, foreign_key="nightclub.id")
    foodcourt_id: Optional[uuid.UUID] = Field(default=None, foreign_key="foodcourt.id")
    qsr_id: Optional[uuid.UUID] = Field(default=None, foreign_key="qsr.id")
    restaurant_id: Optional[uuid.UUID] = Field(default=None, foreign_key="restaurant.id")

class CarouselPoster(CarouselPosterBase, table=True):
    __tablename__ = "carousel_poster"    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    h3_index: str = Field(nullable=False)

    # Relationships [Optional]
    event: Optional["Event"] = Relationship(back_populates="carousel_posters")
    nightclub: Optional["Nightclub"] = Relationship(back_populates="carousel_posters")
    foodcourt: Optional["Foodcourt"] = Relationship(back_populates="carousel_posters")
    qsr: Optional["QSR"] = Relationship(back_populates="carousel_posters")
    restaurant: Optional["Restaurant"] = Relationship(back_populates="carousel_posters")

    @classmethod
    def from_create_schema(cls, db: Session, poster_create: CarouselPosterCreate) -> "CarouselPoster":
        h3_index = None
        if poster_create.nightclub_id:
            h3_index = fetch_h3_index(db, Nightclub, poster_create.nightclub_id)
        elif poster_create.restaurant_id:
            h3_index = fetch_h3_index(db, Restaurant, poster_create.restaurant_id)
        elif poster_create.foodcourt_id:
            h3_index = fetch_h3_index(db, Foodcourt, poster_create.foodcourt_id)
        else:
            h3_index = fetch_h3_index(db, QSR, poster_create.qsr_id)

        return cls(
            image_url=poster_create.image_url,
            deep_link=poster_create.deep_link,
            expires_at=poster_create.expires_at,
            event_id=poster_create.event_id,
            nightclub_id=poster_create.nightclub_id,
            foodcourt_id=poster_create.foodcourt_id,
            qsr_id=poster_create.qsr_id,
            restaurant_id=poster_create.restaurant_id,
            h3_index=h3_index
        )

    def to_read_schema(self) -> CarouselPosterRead:
        return CarouselPosterRead(
            id=self.id,
            image_url=self.image_url,
            deep_link=self.deep_link,
            expires_at=self.expires_at,
            event_id=self.event_id,
            nightclub_id=self.nightclub_id,
            foodcourt_id=self.foodcourt_id,
            qsr_id=self.qsr_id,
            restaurant_id=self.restaurant_id,
            h3_index=self.h3_index
        )
