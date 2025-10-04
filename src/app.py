from fastapi import FastAPI
from .routes.images import router as images_router
import logging
from .utils.logger import get_logger

app = FastAPI(title="EMF to PNG Converter")

app.include_router(images_router)