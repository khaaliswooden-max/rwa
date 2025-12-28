#!/usr/bin/env python3
"""Database initialization script.

Creates all database tables and optionally loads sample data.

Usage:
    python scripts/init_db.py [--sample-data] [--drop-existing]

Options:
    --sample-data    Load sample data for development/testing
    --drop-existing  Drop existing tables before creating (DANGEROUS!)
"""

import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def init_database(drop_existing: bool = False, load_sample: bool = False) -> None:
    """Initialize the database."""
    from src.models.database import Base, drop_db, engine, init_db
    from src.models.schemas import (
        MeterReading,
        Obligation,
        Pump,
        User,
        WaterSystem,
    )

    print("Initializing RWA database...")

    if drop_existing:
        print("WARNING: Dropping existing tables...")
        drop_db()

    print("Creating tables...")
    init_db()

    if load_sample:
        print("Loading sample data...")
        load_sample_data()

    print("Database initialization complete!")


def load_sample_data() -> None:
    """Load sample data for development."""
    from api.auth import hash_password
    from src.models.database import SessionLocal
    from src.models.schemas import (
        MeterReading,
        Obligation,
        Pump,
        User,
        WaterSystem,
    )

    db = SessionLocal()

    try:
        # Create sample water system
        water_system = WaterSystem(
            name="Sample Rural Water District",
            pwsid="TX1234567",
            state="TX",
            population_served=2500,
            service_connections=850,
            system_type="community",
            total_pipe_length_km=45.0,
            storage_capacity_m3=1500.0,
            production_capacity_m3_day=2000.0,
            address="123 Water St, Ruralville, TX 75001",
            phone="(555) 123-4567",
            email="water@ruralville.gov",
        )
        db.add(water_system)
        db.flush()

        # Create sample user
        admin_user = User(
            email="admin@example.com",
            hashed_password=hash_password("changeme"),
            full_name="System Administrator",
            role="admin",
            water_system_id=water_system.id,
        )
        db.add(admin_user)

        operator_user = User(
            email="operator@example.com",
            hashed_password=hash_password("changeme"),
            full_name="Water Operator",
            role="operator",
            water_system_id=water_system.id,
        )
        db.add(operator_user)

        # Create sample pumps
        pumps = [
            Pump(
                water_system_id=water_system.id,
                pump_id="PUMP-001",
                name="Main Well Pump",
                location="Well House #1",
                pump_type="submersible",
                flow_rate_m3h=50.0,
                head_m=60.0,
                power_kw=22.0,
                rated_efficiency=0.75,
                status="active",
                install_date=datetime(2018, 3, 15),
            ),
            Pump(
                water_system_id=water_system.id,
                pump_id="PUMP-002",
                name="Booster Pump A",
                location="Booster Station",
                pump_type="centrifugal",
                flow_rate_m3h=80.0,
                head_m=40.0,
                power_kw=15.0,
                rated_efficiency=0.72,
                status="active",
                install_date=datetime(2020, 6, 1),
            ),
        ]
        db.add_all(pumps)

        # Create sample obligations
        today = date.today()
        obligations = [
            Obligation(
                water_system_id=water_system.id,
                obligation_id="OBL-001",
                title="Monthly Coliform Sampling",
                description="Collect and submit total coliform samples",
                regulation="EPA SDWA 40 CFR 141.21",
                category="monitoring",
                frequency="Monthly",
                due_date=datetime(today.year, today.month, 15),
                status="pending",
                responsible_party="Operator",
            ),
            Obligation(
                water_system_id=water_system.id,
                obligation_id="OBL-002",
                title="Monthly Operating Report",
                description="Submit monthly operating report to state",
                regulation="State Regulation",
                category="reporting",
                frequency="Monthly",
                due_date=datetime(today.year, today.month, 28),
                status="pending",
                responsible_party="Operator",
            ),
            Obligation(
                water_system_id=water_system.id,
                obligation_id="OBL-003",
                title="Consumer Confidence Report",
                description="Annual water quality report to customers",
                regulation="EPA SDWA 40 CFR 141.151",
                category="reporting",
                frequency="Annual",
                due_date=datetime(today.year, 7, 1),
                status="pending",
                responsible_party="Manager",
            ),
        ]
        db.add_all(obligations)

        # Create sample meter readings (last 30 days)
        import random

        for day_offset in range(30):
            reading_date = datetime.now() - timedelta(days=day_offset)
            # Production meter
            db.add(
                MeterReading(
                    water_system_id=water_system.id,
                    meter_id="PROD-001",
                    meter_type="production",
                    reading_time=reading_date,
                    reading_value=175000 + random.uniform(-10000, 15000),
                    unit="gallons",
                    source="scada",
                    quality_flag="normal",
                )
            )

        db.commit()
        print("Sample data loaded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error loading sample data: {e}")
        raise
    finally:
        db.close()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Initialize RWA database")
    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="Load sample data for development",
    )
    parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop existing tables before creating",
    )
    args = parser.parse_args()

    if args.drop_existing:
        confirm = input(
            "WARNING: This will delete all existing data. Type 'yes' to confirm: "
        )
        if confirm.lower() != "yes":
            print("Aborted.")
            sys.exit(1)

    init_database(
        drop_existing=args.drop_existing,
        load_sample=args.sample_data,
    )


if __name__ == "__main__":
    main()

