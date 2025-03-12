from fastapi import WebSocket
from typing import Dict, List, cast, Any
from uuid import uuid4
from datetime import datetime
from sqlalchemy import and_
from core.dependencies import db_dependency
from models.userModels import User
from core.cachemanager import CacheManager
from models.websocketModel import Message

def genProfileName(full_name: str) -> str:
    words = full_name.split()
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[-1][0]).upper()

cacheManager = CacheManager()

class ConnectionManager:
    def __init__(self):
        self.activeConnections: Dict[int, Dict[str, Any]] = {}
        

    async def connect(self, websocket: WebSocket, userId: int, db:db_dependency):
        userInfo = cacheManager.getUser(userId, db)
        if not userInfo:
            print(f"User {userId} not found")
            return
        
        connectionId = str(uuid4())

        # Add/update active connection
        if userId not in self.activeConnections:
            self.activeConnections[userId] = {
                **userInfo,
                "isActive": True,
                "activeOn": datetime.utcnow(),
                "connectedList": [{"connectionId": connectionId, "websocket": websocket}],
                "newMessages": self.getUnseenMessages(userId, db)
            }
        else:
            self.activeConnections[userId]["isActive"] = True
            self.activeConnections[userId]["activeOn"] = datetime.utcnow()
            self.activeConnections[userId]["connectedList"].append({"connectionId": connectionId, "websocket": websocket})
            self.activeConnections[userId]["newMessages"] = self.getUnseenMessages(userId, db)

        print(f"User {userId} connected with connection id {connectionId}")
        self.getActiveUsers(db)
        return connectionId

    def disconnect(self, connectionId: str, userId: int, db:db_dependency):
        if userId in self.activeConnections:
            connectedList = self.activeConnections[userId].get("connectedList", [])
            filteredList = [conn for conn in connectedList if conn["connectionId"] != connectionId]
            if filteredList:
                self.activeConnections[userId]["connectedList"] = filteredList
                print(f"Removed connection {connectionId} for user {userId}")
            else:
                self.activeConnections[userId]["isActive"] = False
                self.activeConnections[userId]["activeOn"] = datetime.utcnow()
                self.activeConnections[userId]["connectedList"] = []
                print(f"Updated user {userId} to inactive")

        print(f"Connection {connectionId} disconnected")
        self.getActiveUsers(db)

    def is_active(self, userId: int) -> bool:
        return bool(userId in self.activeConnections and self.activeConnections[userId]["isActive"])

    async def send_personal_message(self, message: str, fromUser: int, toUser: int, db: db_dependency):
        try:
            newMessage = Message(userId=toUser, fromUser=fromUser, toUser=toUser, message=message, seen=False)
            db.add(newMessage)
            db.commit()
            db.refresh(newMessage)

            userInfo = self.activeConnections.get(toUser)
            if userInfo and userInfo["isActive"]:
                for connection in userInfo.get("connectedList", []):
                    websocket = connection["websocket"]
                    if websocket.client_state.name == "CONNECTED":
                        await websocket.send_json({"action": "message", "fromUser": fromUser, "message": message})
                        print(f" Sent message from {fromUser} to {toUser}")
                        return {"message": "success", "isDelivered": True}
            print(f" User {toUser} is not active")
            return {"message": "success", "isDelivered": False}

        except Exception as e:
            db.rollback()
            print(f" Failed to send message from {fromUser} to {toUser}: {e}")
            return {"message": "failed", "isDelivered": False}

    async def broadcast(self, message: str):
        for userInfo in self.activeConnections.values():
            if userInfo["isActive"]:
                websocket = cast(WebSocket, userInfo["websocket"])
                if websocket.client_state.name == "CONNECTED":
                    try:
                        await websocket.send_json({"info": message})
                    except Exception as e:
                        print(f"Failed to send message to {userInfo['userId']}: {e}")

    def getActiveUsers(self, db:db_dependency):
        activeUsersList = [
            {
                "userId": userId,
                "username": info.get("username"),
                "profile_name": info.get("profile_name"),
                "isActive": info["isActive"],
                "activeOn": cast(datetime, info["activeOn"]).isoformat(),
                "connectedList": [conn["connectionId"] for conn in info["connectedList"]],
                "newMessages": self.getUnseenMessages(userId, db)
            }
            for userId, info in self.activeConnections.items() if info["isActive"]
        ]
        print(f"Active users: {activeUsersList}")
        return activeUsersList
    
    def getUnseenMessages(self, userId: int, db: db_dependency):
        return db.query(Message).filter(Message.toUser == userId, Message.seen == False).count()

        
    def getMessageHistory(self, userId: int, otherUserId: int, db: db_dependency):
        try:
            print(f"Fetching chat history between {userId} and {otherUserId}")
            messages = db.query(Message).filter(
                ((Message.fromUser == userId) & (Message.toUser == otherUserId)) |
                ((Message.fromUser == otherUserId) & (Message.toUser == userId))
            ).order_by(Message.sentOn.asc()).all()

            # if not messages:
            #     print(f"No messages found between {userId} and {otherUserId}")

            unseen_messages = db.query(Message).filter(
                Message.toUser == userId,
                Message.fromUser == otherUserId,
                Message.seen == False
            ).all()

            for msg in unseen_messages:
                msg.seen = True

            db.commit()

            messageData = [
                {
                    "messageId": msg.mId,
                    "fromUser": msg.fromUser,
                    "toUser": msg.toUser,
                    "message": msg.message,
                    "sentOn": msg.sentOn.isoformat(),
                    "seen": msg.seen
                }
                for msg in messages
            ]
            print(f"Fetched {len(messageData)} messages")
            return messageData

        except Exception as e:
            print(f"Database error: {str(e)}")
            return []

    # def getAllUsers(self, db: db_dependency):
        try:
            users = db.query(User).all()
            allUsersList = [
                {
                    "userId": int(getattr(user, 'id', 0)),
                    "username": getattr(user, 'username', ''),
                    "profile_name": getattr(user, 'profile_name', ''),
                    "isActive": self.is_active(int(getattr(user, 'id', 0))),
                    "activeOn": self.activeConnections.get(int(getattr(user, 'id', 0)), {}).get("activeOn"),
                    "connectedList": [conn["connectionId"] for conn in self.activeConnections.get(int(getattr(user, 'id', 0)), {}).get("connectedList", [])],
                    "newMessages": self.getUnseenMessages(int(getattr(user, 'id', 0)), db)
                }
                for user in users
            ]
            print(f"All users: {allUsersList}")
            return allUsersList
        except Exception as e:
            print(f"Failed to fetch all users: {e}")
            return []

    def userUpdate(self, user:User):
        cacheManager.updateUserCache(user)#update cache