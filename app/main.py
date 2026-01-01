"""
main.py
---------
FastAPI Portfolio App for Mohammad Sajid Vagh
"""

import os
import logging
from datetime import date, datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import Base, engine, SessionLocal
from app import crud, schemas, seed_data
from sqlalchemy import text


def add_project_nickname_column():
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE projects
            ADD COLUMN IF NOT EXISTS project_nickname VARCHAR(255);
        """))
        conn.commit()


# ==========================================================
#                DATABASE INIT
# ==========================================================

Base.metadata.create_all(bind=engine)

# ==========================================================
#                LOGGING SETUP
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("PortfolioApp")


# ==========================================================
#                LIFESPAN HANDLER
# ==========================================================

@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("🚀 Running startup seeding...")
    db = SessionLocal()
    try:
        projects = seed_data.get_seed_projects()
        crud.sync_projects_with_seed(db, projects)
        logger.info("✅ Database seeded successfully!")
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
    finally:
        db.close()

    # Log registered routes
    logger.info("📜 Registered Routes:")
    for route in _app.routes:
        if isinstance(route, APIRoute):
            methods = ', '.join(route.methods)
            logger.info(f"➡️ Route registered: {route.path} | methods=[{methods}] | name={route.name}")
    yield
    logger.info("🛑 Application shutting down...")


# ==========================================================
#                APP INIT
# ==========================================================

app = FastAPI(
    title="Mo.Sajid Portfolio API",
    description="FastAPI backend for portfolio management",
    lifespan=lifespan,
)

# ==========================================================
#                STATIC & TEMPLATE SETUP
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ==========================================================
#            DATABASE DEPENDENCY
# ==========================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
#                UTILS
# ==========================================================

def calculate_age(birthdate: date) -> int:
    today = date.today()
    return today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
    )


# ==========================================================
#                HTML ROUTES
# ==========================================================


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "details": {
            "name": "Mohammad Sajid Vagh",
            "intro": "A Passionate Python Developer 🐍🚀",
        },
        "projects": projects
    })


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    birthdate = datetime.strptime("2002-04-26", "%Y-%m-%d").date()
    return templates.TemplateResponse("about.html", {
        "request": request,
        "details": {
            "name": "Mohammad Sajid Vagh",
            "birth_date": "April 26, 2002",
            "age": calculate_age(birthdate),
            "degree": "Bachelor of Computer Applications (BCA)",
            "city": "Himmatnagar, Gujarat, India",
            "email": "vaghmohammadsajid8@gmail.com",
            "phone": "+91 8980331323",
            "intro": "A Passionate Python Developer 🐍🚀",
        }
    })


@app.get("/skills", response_class=HTMLResponse)
async def skills(request: Request):
    return templates.TemplateResponse("skills.html", {
        "request": request,
        "details": {
            "name": "Mohammad Sajid Vagh",
            "intro": "A Passionate Python Developer 🐍🚀",
        },
    })


@app.get("/projects-details/{pro_id}", response_class=HTMLResponse)
async def detailsProjects(request: Request, pro_id: int, db: Session = Depends(get_db)):
    project_details = crud.get_projects_by_id(db, pro_id)
    projects = crud.get_projects(db)
    print("link is a projects details :", project_details.images[0].image_path)
    return templates.TemplateResponse("details_projects.html", {
        "request": request,
        "details": {
            "name": "Mohammad Sajid Vagh",
            "intro": "A Passionate Python Developer 🐍🚀",
        },
        "project_detail": project_details,
        "projects": projects
    })


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "details": {
            "name": "Mohammad Sajid Vagh",
            "intro": "A Passionate Python Developer 🐍🚀",
        },
    })


@app.get("/projects", response_class=HTMLResponse)
async def get_projects_page(request: Request, db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    return templates.TemplateResponse("projects.html",
                                      {"request": request, "details": {
                                          "name": "Mohammad Sajid Vagh",
                                          "intro": "A Passionate Python Developer 🐍🚀",
                                      },
                                       "projects": projects})


# ==========================================================
#                PROJECT CRUD ROUTES
# ==========================================================


@app.get("/api/projects", response_model=list[schemas.Project])
def api_get_all_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)


@app.post("/api/projects", response_model=schemas.Project)
def api_create_or_update_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    logger.info(f"🛠 Upsert project: {project.project_name}")
    return crud.create_or_update_project(db, project)


@app.delete("/api/projects/{pro_id}")
def api_delete_project(pro_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_project(db, pro_id)
    if not deleted:
        raise StarletteHTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


# ==============================================
#        CATCH ALL ROUTE (404 FALLBACK)
# ==============================================

@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"❌ HTTP {exc.status_code} → {request.url}")

    # 👉 Ignore Chrome DevTools auto-request
    if "/.well-known/appspecific/com.chrome.devtools.json" in str(request.url):
        return HTMLResponse(status_code=204)  # No Content (fully silent)

    # Normal 404
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    # Other errors
    return HTMLResponse(str(exc.detail), status_code=exc.status_code)


# ==============================================
#            RUN SERVER
# ==============================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8004, reload=True)
