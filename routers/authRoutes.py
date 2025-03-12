from fastapi import APIRouter, Depends, HTTPException, status
from core.dependencies import db_dependency
from models.userModels import User
from schemas.userSchema import UserSchema, Approval
from schemas.authSchema import Login
from middleware.auth import renewToken, createRefreshToken, createAccessToken
from utils import comon
from core.webmanager import genProfileName

from utils.encryptDecrypt import  hashPassword, verifyPassword

router = APIRouter(
    tags=["Auth"],
    responses={404: {"Description": "Not found"}},
)

@router.post("/signup")
async def signup(req: UserSchema, db: db_dependency):
    try:

        existing_user = db.query(User).filter(User.username == req.username).first()
        if existing_user:
                return {"error": True, "message": "Username already exists"}
        profileName = genProfileName(req.fullName)
        hashedpasswd = hashPassword(req.password)
            
        new_user = User(
            username=req.username,
            password=hashedpasswd,
            full_name=req.fullName,
            email_id=req.emailId,
            phone_number=req.phoneNumber,
            authkey=req.password,
            user_role=4,
            is_approved=False,
            ref_by=req.refby,
            profile_name=profileName
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        refToken = comon.generateToken(new_user.id, req.username)
        new_user.ref_code = refToken
        db.commit()

        return {"error": False, "message": "succcess"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")

@router.post("/approval")
async def approval(request: Approval, db: db_dependency):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # if user.is_approved:
    #     return {"message": f"User '{user.username}' is already approved."}

    user.is_approved = request.is_approved
    db.commit()

    if request.is_approved:
        status_message = "approved"
    else:
        status_message = "disapproved"
        
    return {"message": f"User '{user.username}' has been {status_message}."}


@router.post("/login")
async def login(req: Login, db: db_dependency):
    try:
        userList = db.query(User).filter(User.username == req.username)
        user = userList.first()

        if not user:
            return {"error": True, "message": "No user found"}
        
        if not user.is_approved:
            return {"error": True, "message": "Approval pending. Contact admin for access."}

        isValidPassword = verifyPassword(req.password, user.password)
        if not isValidPassword:
            return {"error": True, "message": "Invalid credentials"}
        
        data = {
            'userId': user.id,
            'username': user.username,
            'user_role': user.user_role,
        }

        accesstoken = createAccessToken(data)
        refreshtoken = createRefreshToken(data)

        user.access_token = accesstoken
        user.refresh_token = refreshtoken
        db.commit()

        return {"userId": user.id, "accessToken": accesstoken, "refreshToken": refreshtoken}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in server: {str(e)}"
        )

@router.get("/users/approved")
async def get_approved_users(db: db_dependency):
    approved_users = db.query(User).filter(User.is_approved == True).all()
    return {"approved_users": [{"id": user.id, "username": user.username} for user in approved_users]}

@router.get("/users/pending")
async def get_pending_users(db: db_dependency):
    pending_users = db.query(User).filter(User.is_approved == False).all()
    return {"pending_users": [{"id": user.id, "username": user.username} for user in pending_users]}

@router.post("/refreshtoken")
async def refreshToken(tokenData: dict = Depends(renewToken)):
    return tokenData
