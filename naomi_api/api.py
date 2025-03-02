import os
from contextlib import asynccontextmanager
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, initialize_app  # type: ignore[import]
from naomi_core.db import WebhookEvent, initialize_db, session_scope
from pydantic import BaseModel

from naomi_api.notifications import router as notifications_router

cred = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global cred
    initialize_db()

    # Create credentials dict from environment variables
    cred_dict = {
        "type": os.environ.get("FIREBASE_ADMIN_TYPE"),
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_ADMIN_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_ADMIN_PRIVATE_KEY"),
        "client_email": os.environ.get("FIREBASE_ADMIN_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_ADMIN_CLIENT_ID"),
        "auth_uri": os.environ.get("FIREBASE_ADMIN_AUTH_URI"),
        "token_uri": os.environ.get("FIREBASE_ADMIN_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("FIREBASE_ADMIN_AUTH_PROVIDER_CERT_URL"),
        "client_x509_cert_url": os.environ.get("FIREBASE_ADMIN_CLIENT_CERT_URL"),
        "universe_domain": os.environ.get("FIREBASE_ADMIN_UNIVERSE_DOMAIN"),
    }

    cred = credentials.Certificate(cred_dict)
    initialize_app(cred)
    yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("STREAMLIT_URL", "http://localhost:8501")],
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


# Include the notifications router
app.include_router(notifications_router, prefix="/notifications")


def main():
    # Load environment variables before app initialization
    load_dotenv()

    import argparse

    import uvicorn

    parser = argparse.ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8090, help="Port to run the server on")
    args = parser.parse_args()

    uvicorn.run("naomi_api.api:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
