from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date, datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    details = {'name': 'Mohammad Sajid',
               'detail': 'As a backend developer, I design and maintain the server-side logic that powers web applications.'}
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
        'introduction': 'Hello! My name is MohammadSajid Vagh, a dedicated and detail-oriented IT professional from Gujarat, India. I hold a Bachelor of Computer Applications (BCA) with a remarkable 8.44 CGPA from I.T.Sheliya Jafari B.C.A. College Sidhpur . My academic background, combined with my technical expertise, fuels my passion for solving complex problems and creating efficient solutions in the tech world.',
        'birth_date': 'April 26, 2002', 'age': age,
        'Phone': '+91 8980331323',
        'Degree': 'Bachelor of Computer Applications(BCA)',
        'City': 'Gujarat, India',
        'Email': 'vaghmohammadsajid8@gmail.com'
    }
    return templates.TemplateResponse("about.html", {"request": request, "details": details})


@app.get('/contact', response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})
