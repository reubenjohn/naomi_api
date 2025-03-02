from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, HTTPException, requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from dotenv import load_dotenv

from naomi_core.db import WebhookEvent, initialize_db, session_scope
from firebase_admin import initialize_app, credentials, messaging  # type: ignore[import]

cred = credentials.Certificate(os.environ["SERVICE_ACCOUNT_KEY_PATH"])
initialize_app(cred)

FIREBASE_SERVER_KEY = "YOUR_FIREBASE_SERVER_KEY"
subscribers = []  # Stores FCM tokens


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WebhookEventRequest(BaseModel):
    type: str
    payload: Dict[str, Any]


@app.post("/webhook")
async def receive_webhook(event: WebhookEventRequest):
    with session_scope() as session:
        new_event = WebhookEvent(event_type=event.type, payload=str(event.payload))
        session.add(new_event)
    return {"status": "OK"}


@app.post("/subscribe")
async def subscribe(data: dict):
    token = data.get("token")
    if token not in subscribers:
        subscribers.append(token)
    return {"message": "Subscribed", "token": token}


@app.post("/send_notification")
async def send_notification():
    message = messaging.MulticastMessage(
        data={"score": "850", "time": "2:45"},
        tokens=subscribers,
    )
    response = messaging.send_multicast(message)

    return {"response": "{0} messages were sent successfully".format(response.success_count)}


def main():
    load_dotenv()

    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8090, help="Port to run the server on")
    args = parser.parse_args()

    uvicorn.run("naomi_api.api:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
