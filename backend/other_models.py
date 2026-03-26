from pydantic import BaseModel

class MoveItem(BaseModel):
    assoc_id: int
    location_id: int
