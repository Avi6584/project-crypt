from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from typing import Optional, List, Annotated
from models.userModels import Base
from core.session import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import authRoutes, userRoutes, profileRoutes, manage, mailRoutes, pushRoutes, websocketRoutes
from middleware.auth import authorizeUser
from fastapi.templating import Jinja2Templates

API_PREFIX = "/v1"

origins = ["*"]

def include_router(app):
    app.include_router(authRoutes.router,prefix=API_PREFIX +"/auth")
    app.include_router(userRoutes.router,prefix=API_PREFIX +"/user")
    app.include_router(profileRoutes.router,prefix=API_PREFIX +"/profile")
    app.include_router(manage.router,prefix=API_PREFIX +"/manage")
    app.include_router(mailRoutes.router,prefix=API_PREFIX +"/mail")
    app.include_router(pushRoutes.router,prefix=API_PREFIX +"/notification")
    app.include_router(websocketRoutes.router,prefix=API_PREFIX +"/websocket")


def create_table():
    Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_table()

include_router(app)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    
    if token:
        try:
            token = token.replace("Bearer ", "")
            db: Session = SessionLocal()
            
            try:
                await authorizeUser(token, db=db)
            finally:
                db.close()
                
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e}
            )
    
    response = await call_next(request)
    return response



templates = Jinja2Templates(directory="templates")




if __name__ == '__main__':
    uvicorn.run(app)