from fastapi import APIRouter, WebSocket, Request
from fastapi.websockets import WebSocketDisconnect
from core.webmanager import ConnectionManager
from fastapi.templating import Jinja2Templates
from core.dependencies import db_dependency
from models.websocketModel import Message
from models.userModels import User

router = APIRouter(
    tags=["Websocket"]
)

templates = Jinja2Templates(directory="templates")
manager = ConnectionManager()

@router.get("/getAllMessages")
async def allMessages(db:db_dependency):
        messages = db.query(Message).all()
        return messages


@router.websocket("/communicate/{userId}")
async def websocket_endpoint(websocket: WebSocket, userId: int, db: db_dependency):
    print(f"websocket hit for user {userId}")
    await websocket.accept()

    user = db.query(User).filter(User.id == userId).first()
    if not user:
        print(f"User {userId} not found in DB")
        await websocket.close(code=1008)
        return
    connectionId = await manager.connect(websocket, userId, db)

    # if not connectionId:  # connectionId will be None if the user isn't found
    #     print(f"Closing WebSocket for unknown user {userId}")
    #     await websocket.close(code=1008)
    #     return

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "message":
                recipient_id = data.get("recipient_id")
                message = data.get("message")
                response = await manager.send_personal_message(message, userId, recipient_id, db)
                await websocket.send_json(response)

            elif action == "get_active_users":
                active_users = manager.getActiveUsers(db)
                await websocket.send_json({"action": "active_users", "users": active_users})

            elif action == "get_message_history":
                otherUserId = data.get("otherUserId")
                if not otherUserId or otherUserId == userId:
                    print(f"Invalid otherUserId: {otherUserId}")
                    await websocket.send_json({"action": "message_history", "messages": []})
                    continue
                messages = manager.getMessageHistory(userId, otherUserId, db)
                if not messages:
                    print(f"No messages found between {userId} and {otherUserId}")
                await websocket.send_json({"action": "message_history", "messages": messages})

    except WebSocketDisconnect:
        if connectionId:
            manager.disconnect(connectionId, userId, db)
        if websocket.client_state.name != "CLOSED":
            await websocket.close()
        await manager.broadcast(f"User {userId} disconnected")

@router.get("/active-users")
async def get_active_users(db:db_dependency):
    return manager.getActiveUsers(db)

@router.get("/message-history/{userId}/{otherUserId}")
async def get_message_history(userId: int, otherUserId: int, db: db_dependency):
    return manager.getMessageHistory(userId, otherUserId, db)

# @router.get("/allUsers")
# async def allUsers(db: db_dependency):
#     return manager.getAllUsers(db)

# @router.websocket("/getAllUsers")
# async def websocketUsers(websocket: WebSocket, db: db_dependency):
    try:
        print("Attempting to accept WebSocket connection")
        await websocket.accept()
        all_users = manager.getAllUsers(db)
        await websocket.send_json({"action": "all_users", "users": all_users})
    except Exception as e:
        print(f"Error fetching all users over WebSocket: {e}")
        await websocket.send_json({"action": "error", "message": "Failed to fetch all users"})
    finally:
        if websocket.client_state.name != "CLOSED":
            await websocket.close()