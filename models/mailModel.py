from sqlalchemy import Column, BigInteger, Float, Integer, String,  DECIMAL, Text, Date, Boolean
from core.base_class import Base
from datetime import date

class Mail(Base):
    __tablename__ = "mail_setup"

    id = Column(Integer, primary_key=True, index=True)
    from_mail = Column(String(255), unique=True, nullable=False)
    to_mail = Column(String(255), unique=True, nullable=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    smtp_server = Column(String(150))
    smtp_mail = Column(String(255), unique=True, nullable=False)
    smtp_server_port = Column(Integer)
    subject = Column(String(255))
    body = Column(String(500))
