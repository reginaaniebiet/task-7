import logging
from fastapi import Request

# setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notes-api")

request_count = 0

async def request_counter_middleware(request: Request, call_next):
    global request_count
    request_count += 1
    logger.info(f"Total requests so far: {request_count}")
    response = await call_next(request)
    return response
