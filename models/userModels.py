from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Boolean, CHAR
from core.base_class import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    phone_number = Column(String(15), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    email_id = Column(String(255), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    user_role = Column(Integer, ForeignKey("userroles.id"), nullable=False)
    is_approved = Column(Boolean, default=False)
    authkey = Column(String(60))
    ref_code = Column(String(10))
    ref_by = Column(String(10))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    profile_name = Column(CHAR(2), nullable=False)

    role = relationship('UserRole', back_populates='users')

class UserRole(Base):
    __tablename__ = "userroles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50))

    users = relationship('User', back_populates='role')
