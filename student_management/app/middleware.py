import logging
from fastapi import Request

logging.basicConfig(filename="app/app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

async def log_requests(request: Request, call_next):
    logging.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    return response
