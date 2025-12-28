"""SQLAlchemy database models."""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.models.database import Base


class User(Base):
    """User account model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="operator")  # admin, manager, operator
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    water_system_id = Column(Integer, ForeignKey("water_systems.id"))
    water_system = relationship("WaterSystem", back_populates="users")


class WaterSystem(Base):
    """Water system / utility model."""

    __tablename__ = "water_systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    pwsid = Column(String(20), unique=True, index=True)  # Public Water System ID
    state = Column(String(2))
    population_served = Column(Integer)
    service_connections = Column(Integer)
    system_type = Column(String(50))  # community, non-transient, transient

    # Infrastructure
    total_pipe_length_km = Column(Float)
    storage_capacity_m3 = Column(Float)
    production_capacity_m3_day = Column(Float)

    # Contact
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="water_system")
    pumps = relationship("Pump", back_populates="water_system")
    meter_readings = relationship("MeterReading", back_populates="water_system")
    obligations = relationship("Obligation", back_populates="water_system")


class MeterReading(Base):
    """Meter reading model - time-series data."""

    __tablename__ = "meter_readings"

    id = Column(Integer, primary_key=True, index=True)
    water_system_id = Column(Integer, ForeignKey("water_systems.id"), nullable=False)

    # Meter identification
    meter_id = Column(String(50), index=True, nullable=False)
    meter_type = Column(String(50))  # production, distribution, customer

    # Reading data
    reading_time = Column(DateTime, index=True, nullable=False)
    reading_value = Column(Float, nullable=False)
    unit = Column(String(20), default="m3")

    # Data quality
    source = Column(String(50))  # scada, ami, manual
    quality_flag = Column(String(20))  # normal, estimated, suspect

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    water_system = relationship("WaterSystem", back_populates="meter_readings")


class Pump(Base):
    """Pump asset model."""

    __tablename__ = "pumps"

    id = Column(Integer, primary_key=True, index=True)
    water_system_id = Column(Integer, ForeignKey("water_systems.id"), nullable=False)

    # Identification
    pump_id = Column(String(50), index=True, nullable=False)
    name = Column(String(255))
    location = Column(String(255))

    # Specifications
    pump_type = Column(String(50))  # centrifugal, submersible, etc.
    flow_rate_m3h = Column(Float)
    head_m = Column(Float)
    power_kw = Column(Float)
    rated_efficiency = Column(Float)

    # Status
    status = Column(String(20), default="active")  # active, maintenance, retired
    install_date = Column(DateTime)
    last_maintenance = Column(DateTime)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    water_system = relationship("WaterSystem", back_populates="pumps")


class Obligation(Base):
    """Compliance obligation model."""

    __tablename__ = "obligations"

    id = Column(Integer, primary_key=True, index=True)
    water_system_id = Column(Integer, ForeignKey("water_systems.id"), nullable=False)

    # Identification
    obligation_id = Column(String(50), unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)

    # Regulatory reference
    regulation = Column(String(255))
    category = Column(String(50))  # monitoring, reporting, treatment, operational

    # Timing
    frequency = Column(String(50))
    due_date = Column(DateTime, index=True)
    reminder_days = Column(Integer, default=7)

    # Status
    status = Column(String(20), default="pending")
    completion_date = Column(DateTime)
    notes = Column(Text)

    # Assignment
    responsible_party = Column(String(255))

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    water_system = relationship("WaterSystem", back_populates="obligations")


class SCADAData(Base):
    """SCADA telemetry data - time-series."""

    __tablename__ = "scada_data"

    id = Column(Integer, primary_key=True, index=True)
    water_system_id = Column(Integer, ForeignKey("water_systems.id"), nullable=False)

    # Point identification
    point_id = Column(String(50), index=True, nullable=False)
    point_name = Column(String(255))
    point_type = Column(String(50))  # analog, digital, calculated

    # Data
    timestamp = Column(DateTime, index=True, nullable=False)
    value = Column(Float)
    unit = Column(String(20))
    quality = Column(String(20))

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)


class EnergyUsage(Base):
    """Energy usage data."""

    __tablename__ = "energy_usage"

    id = Column(Integer, primary_key=True, index=True)
    water_system_id = Column(Integer, ForeignKey("water_systems.id"), nullable=False)
    pump_id = Column(Integer, ForeignKey("pumps.id"))

    # Time period
    period_start = Column(DateTime, index=True, nullable=False)
    period_end = Column(DateTime, nullable=False)

    # Energy data
    energy_kwh = Column(Float, nullable=False)
    peak_demand_kw = Column(Float)
    power_factor = Column(Float)

    # Cost
    energy_cost = Column(Float)
    demand_charge = Column(Float)
    total_cost = Column(Float)

    # Metadata
    source = Column(String(50))  # utility_bill, meter, calculated
    created_at = Column(DateTime, default=datetime.utcnow)
