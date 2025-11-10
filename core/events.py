import asyncio
from typing import List, Optional, Any, Dict

_subscribers: List[asyncio.Queue] = []

def subscribe() -> asyncio.Queue:
    queue = asyncio.Queue()
    _subscribers.append(queue)
    return queue

def unsubscribe(queue: asyncio.Queue):
    _subscribers.remove(queue)

def dispatch_event(event: str, payload: Optional[Dict[str, Any]] = None):
    """Broadcast an event to all subscribers with optional payload."""
    event_data = {
        "event": event,
        "payload": payload
    }
    for queue in list(_subscribers):
        queue.put_nowait(event_data)