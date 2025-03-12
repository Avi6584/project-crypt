from passlib.context import CryptContext
from core.dependencies import db_dependency
from models.userModels import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hashPassword(password):
    return pwd_context.hash(password)