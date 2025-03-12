from fastapi import APIRouter, HTTPException, UploadFile, Depends
from core.dependencies import db_dependency
from models.profileModel import Profile
import os
import shutil

router = APIRouter(
    tags=["Profile"]
)

@router.post("/create-profile")
async def create_profile(name: str, email: str, db: db_dependency):
    """Create new user profile."""
    user = Profile(name=name, email=email, profile_pic=None)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Profile created", "user_id": user.id}


@router.get("/profile/{user_id}")
async def get_profile(user_id: int, db: db_dependency):
    """Retrieve user details by user ID."""
    user = db.query(Profile).filter(Profile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/profile-pic/{user_id}")
async def upload_profile_pic(user_id: int, file: UploadFile, db: db_dependency):
    """Change or upload a new profile picture for the user."""
    user = db.query(Profile).filter(Profile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # File handling (save the uploaded file)
    file_location = f"{user_id}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Update profile with the picture path
    user.profile_pic = file_location
    db.commit()
    return {"message": "Profile picture updated", "profile_pic": file_location}