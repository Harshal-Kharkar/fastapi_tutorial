from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

Router = APIRouter(prefix="/sse", tags=["sse"])

@Router.get("/stream")
async def stream(request: Request):
    import asyncio
    import time

    async def event_generator():
        counter = 0
        while True:
            if await request.is_disconnected():
                print("Client disconnected")
                break
            counter += 1
            # Yield as dict for EventSourceResponse
            print("Sending event", counter)
            yield {
                "event": "message",
                "data": f"Message {counter} at {time.strftime('%X')}"
            }
            # Heartbeat event to keep connection alive (optional)
            yield {"event": "ping", "data": "keep-alive"}
            await asyncio.sleep(2)

    return EventSourceResponse(event_generator())