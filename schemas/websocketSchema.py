from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class messageSchema(BaseModel):

    userId: int
    message: str = Field(..., max_length=255)
    fromUser: int 
    toUser: int
    sentOn: datetime
    isDeleted: Optional[bool] = False
    seen:  bool = False
    

    class Config:
        orm_model=True