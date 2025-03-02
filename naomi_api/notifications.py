from collections import defaultdict
import logging

from fastapi import APIRouter, Request
from firebase_admin import messaging  # type: ignore[import]

# Router for notification-related endpoints
router = APIRouter()

# Global variable to store subscribers
subscribers: set[str] = set()


@router.post("")
def subscribe(data: dict):
    token = str(data.get("token"))
    if token not in subscribers:
        subscribers.add(token)
    return {"message": "Subscribed", "token": token}


def send_single_message(token: str, base_url: str) -> bool:
    """Send a single notification to a subscriber using Firebase Admin SDK's message API"""
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title="Test Notification",
                body="This is a test notification from Firebase Cloud Messaging",
            ),
            data={
                "url": base_url,
                "click_action": base_url,
            },
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title="Test Notification",
                    body="This is a test notification from Firebase Cloud Messaging",
                )
            ),
            token=token,
        )

        # Send the message
        message_id = messaging.send(message)
        logging.info(f"Successfully sent notification {message_id=} to token")
        return True

    except Exception as token_error:
        logging.error(f"Error sending to token: {token_error}")
        return False


def send_to_subscribers(subscribers: set[str], base_url: str) -> dict:
    """Send notifications to all subscribers using Firebase Admin SDK's individual message API"""
    if not subscribers:
        logging.warning("No subscribers to send notifications to.")
        return {
            "message": "No subscribers to send notifications to. Enable notifications first.",
            "success_count": 0,
            "failure_count": 0,
        }

    try:
        logging.info(f"Sending notification to {len(subscribers)} subscribers")

        # Track successful sends
        counters: dict[bool, int] = defaultdict(int)

        # Send to each token individually (multicast messages don't work reliably)
        for idx, token in enumerate(subscribers):
            is_success = send_single_message(token, base_url)
            counters[is_success] += 1

        # Return results summary
        return {
            "message": f"Sent {counters[True]} notifications successfully,"
            " {counters[False]} failed",
            "success_count": counters[True],
            "failure_count": counters[False],
        }

    except Exception as e:
        logging.error(f"Error sending notification: {e}")
        return {"message": str(e), "success_count": 0, "failure_count": len(subscribers)}


@router.post("/send")
def send_notification(request: Request):
    """Send notifications to all subscribers"""
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    logging.info(f"Using dynamic base URL for notifications: {base_url}")
    return send_to_subscribers(subscribers, base_url)
