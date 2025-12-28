"""Application configuration management."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "RWA"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    secret_key: str = Field(default="change-me-in-production")

    # API
    # Bind to all interfaces for container/cloud deployment (override via API_HOST env var)
    api_host: str = "0.0.0.0"  # nosec B104
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # CORS - comma-separated list of allowed origins
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = (
        ""  # Additional origins, comma-separated (e.g., "https://app.vercel.app,https://custom.domain.com")
    )

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql://rwa_user:rwa_password@localhost:5432/rwa_dev"
    )
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30

    # JWT Authentication
    jwt_secret_key: str = Field(default="jwt-secret-change-in-production")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Logging
    log_level: str = "INFO"
    log_format: Literal["json", "text"] = "json"
    log_file: str | None = None

    # Feature Flags
    enable_nrw_module: bool = True
    enable_energy_module: bool = True
    enable_compliance_module: bool = True
    enable_offline_mode: bool = True

    # Rate Limiting
    rate_limit_requests_per_minute: int = 60
    rate_limit_burst: int = 10

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
