# app/startup.py

from app.database import SessionLocal
from app import crud, seed_data
import logging

logger = logging.getLogger("Startup")


def run_migrations_and_seed():
    db = SessionLocal()
    try:
        logger.info("🚀 Starting database seed process...")
        # Use the correct function from seed_data.py
        seed_projects = seed_data.get_seed_projects()
        crud.sync_projects_with_seed(db, seed_projects)
        logger.info("✅ Database synced successfully with seed data!")
    except Exception as e:
        logger.exception(f"❌ Error during database seeding: {e}")
    finally:
        db.close()
