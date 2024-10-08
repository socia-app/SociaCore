import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class OrderItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    nightclub_order_id: Optional[uuid.UUID] = Field(default=None, foreign_key="nightclub_order.id")
    restaurant_order_id: Optional[uuid.UUID] = Field(default=None, foreign_key="restaurant_order.id")
    qsr_order_id: Optional[uuid.UUID] = Field(default=None, foreign_key="qsr_order.id")
    item_id: uuid.UUID = Field(foreign_key="menu_item.id", nullable=False)
    quantity: int = Field(nullable=False)
    
    # Relationships
    nightclub_order: Optional["NightclubOrder"] = Relationship(back_populates="order_items")
    restaurant_order: Optional["RestaurantOrder"] = Relationship(back_populates="order_items")
    qsr_order: Optional["QSROrder"] = Relationship(back_populates="order_items")