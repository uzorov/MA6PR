# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import logging

from fastapi import FastAPI
from logging_loki import LokiHandler

from app import rabbitmq

from app.settings import settings

from app.endpoints.book_router import book_catalog_router, metrics_router
from app.endpoints.recommendation_router import recommendation_router

app = FastAPI(title='Book Catalog with Recommendations Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


loki_logs_handler = LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "fastapi"},
    version="1",
)


logger = logging.getLogger("uvicorn.access")
logger.addHandler(loki_logs_handler)

app.include_router(book_catalog_router, prefix='/book-api')
app.include_router(recommendation_router, prefix='/rec-api')
app.include_router(metrics_router)
