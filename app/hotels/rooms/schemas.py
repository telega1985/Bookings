from pydantic import BaseModel
from typing import Optional


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: list[str]
    quantity: int
    image_id: int


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int
