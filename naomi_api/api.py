from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from naomi_core.db import WebhookEvent, initialize_db, session_scope


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(lifespan=lifespan)


class WebhookEventRequest(BaseModel):
    type: str
    payload: Dict[str, Any]


@app.post("/webhook")
async def receive_webhook(event: WebhookEventRequest):
    with session_scope() as session:
        new_event = WebhookEvent(event_type=event.type, payload=str(event.payload))
        session.add(new_event)
    return {"status": "OK"}


def main():
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8090, help="Port to run the server on")
    args = parser.parse_args()

    uvicorn.run("naomi_api.api:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
