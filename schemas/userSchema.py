from pydantic import BaseModel, Field
from typing import Optional

class UserSchema(BaseModel):

    fullName: str = Field(..., max_length=100)
    phoneNumber: str = Field(..., max_length=15)
    username: str = Field(..., max_length=30)
    emailId: str = Field(..., min_length=5, max_length=255) 
    password: str = Field(..., max_length=60)
    userrole: Optional[int]
    isApproved: Optional[bool] = False
    authkey: Optional[str] = Field(None, max_length=60)
    refby: Optional[str] = Field(None)
    # profileName: str = Field(..., max_length=2)
    
    

    class Config:
        orm_model=True

class Approval(BaseModel):
    user_id: int
    is_approved: bool

    class Config:
        orm_model=True

class UserResponse(UserSchema):
    userId: int
    message: str
    accessToken: Optional[str] = Field(None, max_length=255)
    refreshToken: Optional[str] = Field(None, max_length=255)