from typing import List

from fastapi import APIRouter
from firebase_admin import messaging  # type: ignore[import]

# Router for notification-related endpoints
router = APIRouter()

# Global variable to store subscribers
subscribers: List[str] = []


@router.post("")
async def subscribe(data: dict):
    token = str(data.get("token"))
    if token not in subscribers:
        subscribers.append(token)
    return {"message": "Subscribed", "token": token}


@router.post("/send")
async def send_notification():
    message = messaging.MulticastMessage(
        data={"score": "850", "time": "2:45"},
        tokens=subscribers,
    )
    response = messaging.send_multicast(message)

    return {"response": "{0} messages were sent successfully".format(response.success_count)}
