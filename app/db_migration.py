from sqlalchemy import text
from app.database import engine

def run_migrations():
    with engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE projects
            ADD COLUMN IF NOT EXISTS project_nickname VARCHAR(255);
        """))
