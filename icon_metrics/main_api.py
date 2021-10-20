from multiprocessing.pool import ThreadPool

import uvicorn
from fastapi import FastAPI
from fastapi_health import health
from prometheus_client import start_http_server
from starlette.middleware.cors import CORSMiddleware

from icon_metrics.api.health import is_database_online
from icon_metrics.api.v1.router import api_router
from icon_metrics.config import settings
from icon_metrics.http_client import http_client
from icon_metrics.log import logger

app = FastAPI()
app.add_api_route("/health", health([is_database_online]))

tags_metadata = [
    {
        "name": "icon-metrics",
        "description": "...",
    },
]

app = FastAPI(
    title="ICON Metrics Service",
    description="Various metrics to support odd queries for the ICON Tracker.",
    version="v0.1.0",
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.DOCS_PREFIX}/openapi.json",
    docs_url=f"{settings.DOCS_PREFIX}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    http_client.start()


logger.info("Starting metrics server.")
metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))

logger.info("Starting application...")
app.include_router(api_router, prefix=settings.REST_PREFIX)
app.add_api_route(settings.HEALTH_PREFIX, health([is_database_online]))


if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
        debug=True,
        workers=1,
    )
