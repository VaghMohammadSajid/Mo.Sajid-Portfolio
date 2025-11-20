# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# You can use DATABASE_URL from .env or directly define it
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgresql@localhost:5432/Mo_sajid_portfolio")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Dependency to get DB session.
    Automatically closes session after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables and seed default data.
    """
    from app import models
    from app.seed_data import seed_all_data  # <-- from your seed_data.py

    # Create all database tables
    Base.metadata.create_all(bind=engine)

    # Initialize seed data (create/update/delete)
    db = SessionLocal()
    try:
        seed_all_data(db)  # <-- this function will sync data based on seed_data.py and crud.py
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seeding data failed: {e}")
    finally:
        db.close()
