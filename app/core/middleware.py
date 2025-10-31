# app/middleware/logger_middleware.py

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# ===============================
# 🔹 Configurar logger
# ===============================
logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)

# Guardar también en archivo
file_handler = logging.FileHandler("logs/requests.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ===============================
# 🔹 Middleware de logging
# ===============================
class TimerLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Procesar la request
        response = await call_next(request)

        process_time = time.time() - start_time
        formatted_time = f"{process_time:.4f}s"

        log_message = f"{request.method} {request.url.path} completed in {formatted_time}"
        logger.info(log_message)

        return response
