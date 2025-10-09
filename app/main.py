import os.path

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date, datetime
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import logging
from sqlalchemy.orm import Session
from app import schemas, models, crud, seed_data
from app.database import SessionLocal, engine, Base
from app.models import *

# ------------------ Database ------------------
Base.metadata.create_all(engine)

# ------------------ Logging Config ------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")  # Use Uvicorn's logger

# ------------------ FastAPI App ------------------
app = FastAPI()


# ------------------ Dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ Static & Templates ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(BASE_DIR), "templates"))


# ------------------ Startup Event ------------------
@app.on_event("startup")
def startup_event():
    seed_data.seed_projects()
    logger.info("✅ Seed data executed on startup")


# ------------------ CRUD Routes ------------------
@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_projects(db=db, projects=project)


@app.get("/projects/{pro_id}", response_model=schemas.Project)
def project_read(pro_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_projects(db=db, pro_id=pro_id)
    if not db_project:
        raise StarletteHTTPException(status_code=404, detail="Project not found")
    return db_project


# ------------------ Middleware ------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method == "GET" and not request.url.path.startswith("/static"):
        logger.info(f"➡️ Page visited: {request.url.path}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.exception(f"❌ Unhandled error for {request.url.path}: {e}")
        return HTMLResponse("Internal Server Error", status_code=500)


# ------------------ Exception Handlers ------------------
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"🚨 HTTP {exc.status_code} error at {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# ------------------ Utils ------------------
class BirthDateInput(BaseModel):
    birthdate: date


def calculate_age(data: BirthDateInput):
    today = date.today()
    birthdate = data.birthdate
    return today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
    )


# ------------------ Routes ------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    details = {
        'name': 'Mohammad Sajid',
        'detail': 'As a backend developer, I design and maintain the server-side logic that powers web applications.'
    }
    return templates.TemplateResponse("index.html", {"request": request, "details": details})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    birth_date_obj = datetime.strptime('2002-04-26', '%Y-%m-%d').date()
    age = calculate_age(BirthDateInput(birthdate=birth_date_obj))
    details = {
        'name': "Mohammad Sajid Vagh",
        'birth_date': 'April 26, 2002',
        'age': age,
        'Phone': '+91 8980331323',
        'Degree': 'Bachelor of Computer Applications',
        'City': 'Gujarat, India',
        'Email': 'vaghmohammadsajid8@gmail.com',
        'introduction': (
            "I’m a Python developer with a BCA degree and hands-on experience "
            "building backend features using Django, REST APIs, and relational databases."
        )
    }
    logger.info(f"🎓 Degree: {details['Degree']}")
    return templates.TemplateResponse("about.html", {"request": request, "details": details})


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, db: Session = Depends(get_db)):
    projects_orm = crud.get_projects(db)  # returns all Projects
    projects = [schemas.Project.from_orm(p) for p in projects_orm]  # convert to Pydantic

    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects}
    )


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


# ------------------ Main ------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
