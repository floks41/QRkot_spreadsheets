"""Основной модуль проекта CAT_CHARITY_FUND на фреймворке FastAPI."""


import logging
from fastapi import FastAPI

from app.api.router import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """При запуске приложения создает суперпользователя
    (при его отсутствии)."""
    logging.basicConfig(level=logging.INFO)
    await create_first_superuser()
