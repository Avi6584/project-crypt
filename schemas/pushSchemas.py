from pydantic import BaseModel
from typing import Optional
from datetime import date

class SubscriptionSchema(BaseModel):
    user_id: int
    endpoint: str
    p256dh: str
    auth: str
    is_deleted: Optional[bool] = False
    subscription_date: Optional[date] = None

    class Config:
        from_attributes = True


class NotificationSchema(BaseModel):
    user_id: int
    title: Optional[str]
    body: str
    icon: Optional[str]
    url: Optional[str]

    class Config:
        from_attributes = True