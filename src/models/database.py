"""Database configuration and session management."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from api.config import get_settings

settings = get_settings()

# Create engine
engine = create_engine(
    str(settings.database_url),
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_pre_ping=True,  # Enable connection health checks
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Declarative base for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Get database session dependency for FastAPI.

    Yields:
        Database session

    Example:
        @app.get("/items")
        async def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Example:
        with get_db_context() as db:
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    # Import all models to ensure they're registered
    from src.models import schemas  # noqa: F401

    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all database tables. Use with caution!"""
    Base.metadata.drop_all(bind=engine)


# TimescaleDB hypertable creation (run after table creation)
TIMESCALE_HYPERTABLES = [
    ("meter_readings", "reading_time"),
    ("scada_data", "timestamp"),
]


def create_hypertables(connection) -> None:
    """
    Create TimescaleDB hypertables for time-series data.

    Should be run after initial table creation.
    """
    for table_name, time_column in TIMESCALE_HYPERTABLES:
        try:
            connection.execute(
                f"SELECT create_hypertable('{table_name}', '{time_column}', "
                f"if_not_exists => TRUE);"
            )
        except Exception as e:
            # Hypertable might already exist or TimescaleDB not installed
            print(f"Note: Could not create hypertable for {table_name}: {e}")
