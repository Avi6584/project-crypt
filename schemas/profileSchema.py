from pydantic import BaseModel
from typing import Optional

class ProfileSchema(BaseModel):
    id: int
    name: str
    email: str
    profile_pic: Optional[str] = None

    class Config:
        orm_mode = True