import asyncio
import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from core.events import subscribe, unsubscribe

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
async def events(request: Request):
    queue = subscribe()

    async def event_stream():
        try:
            while True:
                try:
                    event_data = await asyncio.wait_for(queue.get(), timeout=15.0)
                    event_name = event_data["event"]
                    payload = event_data.get("payload")

                    # Send event type
                    yield f"event: {event_name}\n"

                    # Send payload if exists
                    if payload:
                        yield f"data: {json.dumps(payload)}\n\n"
                    else:
                        yield f"data: \n\n"

                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        except asyncio.CancelledError:
            unsubscribe(queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
