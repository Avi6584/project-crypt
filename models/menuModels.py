from sqlalchemy import Column, Integer, SmallInteger, String, ForeignKey
from core.base_class import Base

class Menu(Base):
    __tablename__ = "menu"

    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String(20), nullable=False)
    menu_icon = Column(String(30), nullable=False)
    menu_url = Column(String(30))
    permissions = Column(String(10), nullable=False)