from fastapi import APIRouter, HTTPException, status
from core.dependencies import db_dependency
from sqlalchemy import Column, Integer, String, select
from models.userModels import User

router = APIRouter(
    tags=["Manage"]
)

@router.get("/owner")
async def get_owners(db: db_dependency):
    owners = db.query(User).filter(User.user_role == 1).all()
    return {
        "owner": [
            {
                "id": owner.id,
                "fullName": owner.full_name,
                "username": owner.username,
                "emailId": owner.email_id,
                "isApproved": owner.is_approved
            }
            for owner in owners
        ]
    }

@router.get("/admin")
async def get_admins(db: db_dependency):
    admins = db.query(User).filter(User.user_role == 2).all()
    return {
        "admin": [
            {
                "id": admin.id,
                "fullName": admin.full_name,
                "username": admin.username,
                "emailId": admin.email_id,
                "isApproved": admin.is_approved
            }
            for admin in admins
        ]
    }

@router.get("/developer")
async def get_developers(db: db_dependency):
    developers = db.query(User).filter(User.user_role == 3).all()
    return {
        "developer": [
            {
                "id": developer.id,
                "fullName": developer.full_name,
                "username": developer.username,
                "emailId": developer.email_id,
                "isApproved": developer.is_approved
            }
            for developer in developers
        ]
    }

@router.get("/user")
async def get_users(db: db_dependency):
    users = db.query(User).filter(User.user_role == 4).all()
    return {
        "user": [
            {
                "id": user.id,
                "fullName": user.full_name,
                "username": user.username,
                "emailId": user.email_id,
                "isApproved": user.is_approved
            }
            for user in users
        ]
    }
