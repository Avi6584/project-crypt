from pywebpush import webpush, WebPushException
import json

VAPID_PUBLIC_KEY = "BB2XtwZN-qFqlW2iIODPx_PYrFnOPOd94VFSUA_MJxF0OmpCFGvq2ocznYR1FShptAXGXXzTq5lHCmSPnmktA98"
VAPID_PRIVATE_KEY = "HhvHjqM5TKyDno48tS7qRCpLZJU-IIZmg48Lx4igkkQ"

def pushNotification(payload: dict):
    try:
        # Extract values from the payload
        sub_info = payload.get("sub_info")
        message = payload.get("body", "Default message")
        title = payload.get("title", "Notification")
        icon = payload.get("icon", "/favicon.ico")
        url = payload.get("url", "/")

        # Convert the message to JSON format
        data = json.dumps({
            "title": title,
            "body": message,
            "icon": icon,
            "url": url
        })
        
        webpush(
            subscription_info=sub_info,
            data=data,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:testavinash216@gmail.com"},
            content_encoding="aesgcm"
        )
        
    except WebPushException as e:
        print(f"Error sending notification: {str(e)}")
        raise Exception(f"Web push failed: {str(e)}")