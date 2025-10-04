from fastapi import FastAPI
from .routes.images import router as images_router
import logging
from .utils.logger import get_logger

# Unify app logging
logger = get_logger("app")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = logger.handlers
uvicorn_access_logger.setLevel(logging.INFO)

# Start app
app = FastAPI(title="EMF to PNG Converter")

app.include_router(images_router)