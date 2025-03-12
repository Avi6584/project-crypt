from sqlalchemy import Column, Integer, SmallInteger, String, ForeignKey
from core.base_class import Base

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    profile_pic = Column(String(200), nullable=True)