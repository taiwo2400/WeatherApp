#!/usr/bin/env python

import time

import yaml
from openapi_spec_validator import validate

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from backend.app.api.v1.endpoints import router as api_router
from backend.app.utils.logging_config import configure_structlog, get_logger

# Initialize structlog
configure_structlog()

log = get_logger()


def custom_openapi():
    """
    Custom OpenAPI
    :return: openapi schema
    """
    with open("docs/openapi/weather_app.yaml", "r") as file:
        openapi_schema = yaml.safe_load(file)

    # Validate the specification
    try:
        validate(openapi_schema)
        log.info("OpenAPI spec is valid!")
    except Exception as e:
        log.info(f"OpenAPI spec is invalid: {e}")

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def get_application():
    """
    Get FastAPI application instance
    :return: FastAPI app
    """
    app = FastAPI()
    app.openapi = custom_openapi
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")

    # Middleware to log requests and responses
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"

        log.info("Request received", method=request.method,
                 path=request.url.path, ip=client_ip)

        response = await call_next(request)

        duration = time.time() - start_time
        log.info("Response sent", status_code=response.status_code,
                 duration=f"{duration:.4f}s")

        return response

    return app


app = get_application()
