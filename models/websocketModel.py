from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, CHAR
from core.base_class import Base
from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'

    mId = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    message = Column(String(255), nullable=False)
    fromUser = Column(Integer, nullable=False)
    toUser = Column(Integer, nullable=False)
    sentOn = Column(DateTime, default=datetime.utcnow, nullable=False)
    isDeleted = Column(Boolean, default=False)
    seen = Column(Boolean, default=False)