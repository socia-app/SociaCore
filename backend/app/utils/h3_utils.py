import h3
from fastapi import HTTPException
from math import sqrt
from sqlmodel import SQLModel, Session
from typing import Type
import uuid
from .crud import get_record_by_id


def get_h3_index(latitude: float, longitude: float, resolution: int = 9) -> str:
    return h3.latlng_to_cell(latitude, longitude, resolution)

def get_nearby_h3_indexes(origin, radius_km):
    try:
        resolution = 9  # H3 resolution
        hexagon_area_km2 = h3.cell_area(origin, unit='km^2') 
        # Get area of a single hexagon

        # Approximate hexagon radius (radius of the circle enclosing the hexagon)
        hexagon_radius_km = sqrt(2 * hexagon_area_km2 / (3 * sqrt(3)))  # Derived formula

        # Calculate the number of rings (k) based on the input radius
        k_rings = int(radius_km / hexagon_radius_km)  # Estimate number of rings

        # Get all H3 indexes within k-rings
        h3_indexes = h3.grid_disk(origin, k_rings)

        return h3_indexes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving nearby H3 indexes")



def fetch_h3_index(session: Session, model: Type[SQLModel], id: uuid.UUID):
    record = get_record_by_id(session, model, id).dict()

    return record.get("h3_index", None)