from fastapi import HTTPException, Request

async def enforce_user_agent_header(request: Request, call_next):
    # Header keys are case-insensitive; FastAPI exposes lowercase dict-like access.
    if "user-agent" not in request.headers or not request.headers.get("user-agent"):
        # Explicitly reject if User-Agent missing/empty
        raise HTTPException(status_code=400, detail="User-Agent header required")
    response = await call_next(request)
    return response
