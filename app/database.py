# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app import models
    from app.seed_data import seed_all_data

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_all_data(db)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seeding data failed: {e}")
    finally:
        db.close()
