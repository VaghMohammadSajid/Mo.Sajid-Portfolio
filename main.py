from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date, datetime
import uvicorn
import logging

# ------------------ Logging Config ------------------
logger = logging.getLogger("uvicorn")   # use uvicorn's logger
# ----------------------------------------------------

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Middleware to log all GET page requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method == "GET" and not request.url.path.startswith("/static"):
        logger.info(f"➡️ Page visited: {request.url.path}")
    response = await call_next(request)
    return response


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    details = {
        'name': 'Mohammad Sajid',
        'detail': 'As a backend developer, I design and maintain the server-side logic that powers web applications.'
    }
    return templates.TemplateResponse("index.html", {"request": request, "details": details})


class BirthDateInput(BaseModel):
    birthdate: date


def calculate_age(data: BirthDateInput):
    today = date.today()
    birthdate = data.birthdate
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    birth_date_str = '2002-04-26'
    birth_date_obj = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    age = calculate_age(BirthDateInput(birthdate=birth_date_obj))
    details = {
        'name': "MohammadSajid Vagh",
        'introduction': (
            "I’m a Python developer with a BCA degree and hands-on experience "
            "building backend features using Django, REST APIs, and relational databases "
            "such as PostgreSQL and MySQL.\n\n"
            "At Stackerbee Technologies I contributed to web application development — "
            "designing and implementing APIs, writing clean and maintainable code, "
            "improving query performance, and integrating data between services.\n\n"
            "I enjoy solving backend challenges, turning requirements into reliable solutions, "
            "and collaborating with teams to deliver features that scale. I’m open to remote "
            "opportunities where I can grow as a backend engineer and help build modern, efficient web systems.\n\n"
            "Let’s connect if you’re looking for a motivated developer who learns fast and enjoys "
            "building practical solutions."
        ),
        'birth_date': 'April 26, 2002',
        'age': age,
        'Phone': '+91 8980331323',
        'Degree': 'Bachelor of Computer Applications',
        'City': 'Gujarat, India',
        'Email': 'vaghmohammadsajid8@gmail.com'
    }
    logger.info(f"🎓 Degree: {details['Degree']}")
    return templates.TemplateResponse("about.html", {"request": request, "details": details})


@app.get('/project')
async def project(request: Request):
    print("req is :", request)
    return templates.TemplateResponse("project.html", {"request": request})


@app.get('/contact', response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
