"""RWA API - Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import get_settings
from api.routers import compliance, data_ingestion, energy, nrw

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    print(f"Starting {settings.app_name} API...")
    yield
    # Shutdown
    print(f"Shutting down {settings.app_name} API...")


app = FastAPI(
    title=settings.app_name,
    description=(
        "Rural Water Association Digital Transformation Platform API. "
        "Empowering small rural water systems with data-driven operations "
        "through Non-Revenue Water optimization, Energy management, and "
        "Compliance automation."
    ),
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan,
)

# CORS middleware - build list of allowed origins
cors_origins = [settings.frontend_url]
if settings.cors_origins:
    # Add additional origins from comma-separated config
    cors_origins.extend(
        origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "0.1.0",
        "environment": settings.app_env,
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name} API",
        "docs": "/docs",
        "version": "0.1.0",
    }


# Include routers with API prefix
if settings.enable_nrw_module:
    app.include_router(
        nrw.router,
        prefix=f"{settings.api_prefix}/nrw",
        tags=["Non-Revenue Water"],
    )

if settings.enable_energy_module:
    app.include_router(
        energy.router,
        prefix=f"{settings.api_prefix}/energy",
        tags=["Energy Management"],
    )

if settings.enable_compliance_module:
    app.include_router(
        compliance.router,
        prefix=f"{settings.api_prefix}/compliance",
        tags=["Compliance"],
    )

app.include_router(
    data_ingestion.router,
    prefix=f"{settings.api_prefix}/data",
    tags=["Data Ingestion"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "type": type(exc).__name__,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.is_development,
    )
