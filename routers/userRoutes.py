from fastapi import APIRouter, HTTPException, status
from core.dependencies import db_dependency
from typing import Optional
from models.userModels import User, UserRole
from schemas.userSchema import UserSchema
from schemas.menuSchemas import MenuSchema
from models.menuModels import Menu
from utils.encryptDecrypt import  hashPassword, verifyPassword
from core.webmanager import genProfileName

router = APIRouter(
    tags=["User"]
)

# Function to update profile name in User table
def profileNames(db: db_dependency):
    users = db.query(User).all()
    for user in users:
        if not user.profile_name:
            user.profile_name = genProfileName(user.full_name)
            print(f"Updated profile name for {user.full_name} -> {user.profile_name}")

    db.commit()

@router.get("/getAllUsers")
async def get_all_users(db:db_dependency):
        users = db.query(User).all()
        return users


@router.post("/registerUser")
async def register_user(req: UserSchema, db:db_dependency):
    try:
        existingEmail = db.query(User).filter(User.email_id == req.emailId).first()
        if existingEmail:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        
        # Generate profile name if not provided
        profileName = genProfileName(req.fullName)

        hashedpasswd = hashPassword(req.password)
        addUser = User(
            full_name = req.fullName,
            phone_number = req.phoneNumber,
            username = req.username,
            email_id = req.emailId,
            password = hashedpasswd,
            user_role = req.userrole,
            authkey=req.password,
            profile_name = profileName
        
        )

        db.add(addUser)
        db.commit()
        print(f"User added with profile name: {addUser.profile_name}")
        db.refresh(addUser)
        return {"error": False, "message": "succcess", "userId":addUser.id}
    
    except Exception as e: 
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")


@router.get("/users/{user_Id}")
async def read_user(user_Id: int, db: db_dependency):
            user = db.query(User).filter(User.id == user_Id).first()
            if user is None:
                raise HTTPException(status_code=404, detail='User not found')
            return user


@router.put("/updateuser/{user_id}")
async def updateUser(user_id:int, req:UserSchema, db:db_dependency):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": True, "message": "No user found" }
        else:
            
            user.full_name = req.fullName,
            user.phone_number = req.phoneNumber,
            user.username = req.username,
            user.email_id = req.emailId,
            user.user_role = req.userrole,
            user.profile_name = req.profileName if req.profileName else genProfileName(req.fullName)
            

        if req.password:
            user.password = hashPassword(req.password),
            user.authkey=req.password
                 
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"error": False, "message": "succcess", "userId":user.id}

    except Exception as e: 
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")


@router.delete('/deleteuser/{UserId}')
async def deleteUser(UserId: int, db: db_dependency):
    try:
        users = db.query(User).filter(User.id == UserId).first()

        if not users:
            return {"error": True, "message": "No user found"}
        db.delete(users)
        db.commit()
        

        return {"error": False, "message": "Success"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in server: {str(e)}")


@router.get("/getAllMenus")
async def get_all_menus(db:db_dependency):
        menus = db.query(Menu).all()
        return menus


@router.get("/menuList/{userId}")
async def getMenus(userId: int, db:db_dependency):
    try:

        user = db.query(User).filter(User.id == userId).first()
    
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        role_id = user.user_role

        menus = db.query(Menu).filter(Menu.permissions.contains(str(role_id))).all()
        
        if not menus:
            return {"message": "No menus found for the user_role"}


        menu_list = [
             {
                # "menu_id": menu.menu_id,
                "menu_name": menu.menu_name,
                "menu_icon": menu.menu_icon,
                "menu_url": menu.menu_url,
            }
            for menu in menus
        ]
        return menu_list

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")

@router.get("/userroles")
async def getUserRoles(db:db_dependency):
    list = db.query(UserRole).all()
    return list


@router.get("/getReferal/{uId}")
async def getReferal(uId: int, db:db_dependency):
    try:
        user = db.query(User).filter(User.id == uId).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        referred_users = db.query(User).filter(User.ref_by == user.ref_code, User.id != uId).all()

        return {
            "refCode": user.ref_code,
            "referred_users": referred_users
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error in server: {str(e)}")
    
