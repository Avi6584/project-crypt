from sqlalchemy import Column, BigInteger, Float, Integer, String,  DECIMAL, Text, Date, Boolean
from core.base_class import Base
from datetime import date

class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    endpoint = Column(String(500), nullable=False)
    p256dh = Column(String(255), nullable=False)
    auth = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=False)
    subscription_date = Column(Date, nullable=True)

class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    icon = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)