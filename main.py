from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date, datetime
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import logging

# ------------------ Logging Config ------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")  # Use Uvicorn logger
# ----------------------------------------------------

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------------- Middleware ----------------
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


# ---------------- Exception Handlers ----------------
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"🚨 HTTP {exc.status_code} error at {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# ---------------- Models ----------------
class BirthDateInput(BaseModel):
    birthdate: date


def calculate_age(data: BirthDateInput):
    today = date.today()
    birthdate = data.birthdate
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


# ---------------- Routes ----------------
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    details = {
        'name': 'Mohammad Sajid',
        'detail': 'As a backend developer, I design and maintain the server-side logic that powers web applications.'
    }
    return templates.TemplateResponse("index.html", {"request": request, "details": details})


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    birth_date_obj = datetime.strptime('2002-04-26', '%Y-%m-%d').date()
    age = calculate_age(BirthDateInput(birthdate=birth_date_obj))
    details = {
        'name': "MohammadSajid Vagh",
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


@app.get('/projects', response_class=HTMLResponse)
async def projects(request: Request):
    logger.info("➡️ Projects page visited")
    return templates.TemplateResponse("projects.html", {"request": request})


@app.get('/contact', response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


# ---------------- Main ----------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
