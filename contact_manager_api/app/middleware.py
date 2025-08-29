import logging
from fastapi import Request

logger = logging.getLogger("contact-manager")
logging.basicConfig(level=logging.INFO)

async def ip_logging_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    path = request.url.path
    logger.info(f"[IP {client_ip}] {method} {path}")
    response = await call_next(request)
    return response
