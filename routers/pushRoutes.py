from fastapi import APIRouter, HTTPException, status
from schemas.pushSchemas import SubscriptionSchema, NotificationSchema
from core.dependencies import db_dependency
from models.userModels import User
from models.pushModels import Subscription
from pushService import pushNotification


router = APIRouter(
    tags=["Notification"]
)

subscriptions = []


@router.post("/subscribe/")
async def subscribe(req: SubscriptionSchema, db: db_dependency):
    try:
        
        oldSubscription = db.query(Subscription).filter(Subscription.user_id == req.user_id).first()

        if oldSubscription:

            oldSubscription.endpoint = req.endpoint
            oldSubscription.p256dh = req.p256dh
            oldSubscription.auth = req.auth
            oldSubscription.is_deleted = req.is_deleted
            oldSubscription.subscription_date = req.subscription_date
            db.commit()
            return {"message": "Subscription updated"}
        else:
            
            newSubscription = Subscription(
                user_id=req.user_id,
                endpoint=req.endpoint,
                p256dh=req.p256dh,
                auth=req.auth,
                is_deleted=req.is_deleted,
                subscription_date=req.subscription_date
            )
            db.add(newSubscription)
            db.commit()
            db.refresh(newSubscription)
            return {"message": "Subscription created"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")

@router.get('/getSubscribers')
async def allSubscribers(db:db_dependency):
    subscribers = db.query(Subscription).all()
    return subscribers


@router.post("/send-notification/")
async def sendNotification(req: NotificationSchema, db: db_dependency):
    try:
        # Fetch subscription using user_id and is_deleted flag
        sub = db.query(Subscription).filter(Subscription.user_id == req.user_id, Subscription.is_deleted == False).first()
        
        if not sub:
            raise HTTPException(status_code=404, detail="Subscription not found or deleted")

        # Convert subscription object to a dictionary
        sub_pay = {
            "endpoint": sub.endpoint,
            "keys": {
                "p256dh": sub.p256dh,
                "auth": sub.auth
            }
        }

        # Send notification
        payload = {
            "sub_info": sub_pay,
            "body": req.body,
            "title": req.title,
            "icon": req.icon,
            "url": req.url
        }

        pushNotification(payload)
        
        return {"message": "Notification sent successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error in server: {str(e)}")
