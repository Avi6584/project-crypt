from datetime import datetime, timedelta
from typing import Dict, Optional, cast
from sqlalchemy.orm import Session
from models.userModels import User

class CacheManager:
    def __init__(self):
        self.userCache: Dict[int, Dict[str, object]] = {}
        self.cacheExpiration: Dict[int, datetime] = {}
        self.cache_ttl = timedelta(minutes=10)  # Optional: Cache expires after 10 minutes

    def getUser(self, userId: int, db: Session) -> Optional[Dict[str, object]]:
        # Check if user exists in cache and is still fresh
        if userId in self.userCache and self.cacheExpiration.get(userId, datetime.min) > datetime.utcnow():
            print(f"Fetching user {userId} from cache")
            return self.userCache[userId]

        # Fetch from DB if not cached or expired
        user = db.query(User).filter(User.id == userId).first()
        if user:
            self.updateUserCache(user)
            return self.userCache[userId]
        print(f"user not found in database")
        return None

    def updateUserCache(self, user: User):
        self.userCache[cast(int, user.id)] = {
            "userId": user.id,
            "username": str(user.username),
            "profile_name": str(user.profile_name)
        }
        self.cacheExpiration[cast(int, user.id)] = datetime.utcnow() + self.cache_ttl
        print(f"Updated cache for user {user.id}")

    def clearUserCache(self, userId: int):
        if userId in self.userCache:
            del self.userCache[userId]
            del self.cacheExpiration[userId]
            print(f"Removed user {userId} from cache")
