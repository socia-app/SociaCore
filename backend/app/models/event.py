import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.carousel_poster import CarouselPoster
    from app.models.event_booking import EventBooking
    from app.models.event_offering import EventOffering
    from app.models.venue import Venue




class Event(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    venue_id: uuid.UUID = Field(foreign_key="venue.id", nullable=False)
    title: str = Field(nullable=False)
    start_time: datetime = Field(nullable=False)
    end_time: datetime = Field(nullable=False)
    image_url: str | None = Field(nullable=True)
    age_restriction: int | None = Field(nullable=True)
    dress_code: str | None = Field(nullable=True)

    # Relationships
    venue: Optional["Venue"] = Relationship(back_populates="events")
    offerings: list["EventOffering"] = Relationship(back_populates="event")
    event_bookings: list["EventBooking"] = Relationship(back_populates="event")
    carousel_posters: list["CarouselPoster"] | None = Relationship(back_populates="event")