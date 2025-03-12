from passlib.context import CryptContext
from jose import jwt
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from jose.exceptions import JWTError
from fastapi.security import OAuth2PasswordBearer
from models.userModels import User
from core.config import settings
from core.dependencies import get_db, db_dependency
from schemas.authSchema import TokenRequest


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/token')

error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid token'
)


async def authorizeUser(token: str , db: Session = Depends(get_db)) -> dict:
    try:
        tokenData = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    
        if 'userId' not in tokenData and 'username' not in tokenData and 'mode' not in tokenData:
            raise HTTPException(status_code=400,detail="Invalid token structure")
        
        if tokenData['mode'] != 'access_token':
            raise HTTPException(status_code=400,detail="Invalid token mode")
        
        user = db.query(User).filter(User.id == tokenData['userId']).first()
        if not user:
            raise HTTPException(status_code=400,detail="User not found")

    except JWTError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")
    

async def renewToken(request: TokenRequest, db: db_dependency) -> dict:
    try:
        token = request.token
        print(f"Received token: {token}")
        tokenData = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)

        if 'userId' not in tokenData and 'username' not in tokenData and 'mode' not in tokenData:
            raise HTTPException(status_code=400, detail="Invalid token structure")
        
        if tokenData['mode'] != 'refresh_token':
            raise HTTPException(status_code=400, detail="Invalid token mode")
        
        user = db.query(User).filter(User.id == tokenData['userId']).first()
        if not user or token != user.refresh_token:
            raise HTTPException(status_code=400, detail="User not found")
        
        userData = {'userId': user.id, 'username': user.username}
        accesstoken = createAccessToken(userData)
        refreshToken = createRefreshToken(userData)

        #store the token into database
        user.access_token = accesstoken
        user.refresh_token = refreshToken
        db.commit()

        return {
            'accessToken': accesstoken,
            'refreshToken': refreshToken,
        }

    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")



def createAccessToken(data: dict) -> str:
    encodedPayload = data.copy()
    expiryAcc = datetime.utcnow() + settings.JWT_ACCESS_EXP
    encodedPayload.update({'exp': expiryAcc, 'mode': 'access_token'})
    if not isinstance(settings.JWT_SECRET, str) or not settings.JWT_SECRET:
        raise ValueError("JWT_SECRET is not a valid string.")
    return jwt.encode(encodedPayload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def createRefreshToken(data: dict) -> str:
    encodedPayload = data.copy()
    expiryRef = datetime.utcnow() + settings.JWT_REFRESH_EXP
    encodedPayload.update({'exp': expiryRef, 'mode': 'refresh_token'})
    return jwt.encode(encodedPayload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
