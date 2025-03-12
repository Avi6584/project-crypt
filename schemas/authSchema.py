from typing import Optional
from pydantic import BaseModel, Field


class Login(BaseModel):
    username:str = Field(..., max_length=30)
    password: str = Field(..., max_length=60)


class RegisterBase(BaseModel):
    user_name: str
    phone_no: str
    p_word: str



class TokenRequest(BaseModel):
    token: str