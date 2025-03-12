from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class MailSchema(BaseModel):  
    from_mail: str = Field(..., min_length=5, max_length=255)
    to_mail: Optional[str] = Field(..., min_length=5, max_length=255)
    username: str = Field(..., max_length=30)
    password: str = Field(..., max_length=60)
    smtp_server: str = Field(..., max_length=60)
    smtp_mail: str = Field(..., min_length=5, max_length=255)
    smtp_server_port: int
    subject: str = Field(..., max_length=255)
    body : str = Field(..., max_length=500)

    class Config:
        from_attributes = True
