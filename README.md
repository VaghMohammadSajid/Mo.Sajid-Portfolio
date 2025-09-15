# Mo.Sajid-Portfolio

A personal portfolio site showcasing my skills, projects, and professional background.

---

## 🚀 Overview

This website is my digital presence — built to feature who I am, what I do, and what I’ve built. It highlights projects, talks about my expertise, and provides ways to get in touch.

---

## 🛠 Tech Stack

- Python  
- HTML / CSS / JavaScript  
- Flask / (or Django if you're using it)  
- Templating: Jinja2 (or your chosen one)  
- Dependencies listed in `requirements.txt`

---

## 📁 Structure

| Folder / File | Purpose |
|---------------|---------|
| `templates/`  | HTML template files |
| `static/`     | CSS, JS, images, other static assets |
| `main.py`     | Entry point for running the app |
| `requirements.txt` | List of Python packages needed |

---

## 🔧 Setup & Running Locally

```bash
# clone project
git clone https://github.com/VaghMohammadSajid/Mo.Sajid-Portfolio.git
cd Mo.Sajid-Portfolio

# create & activate venv
python -m venv env
source env/bin/activate     # macOS / Linux
# .\env\Scripts\activate    # Windows

# install & run
pip install -r requirements.txt
cp .env.example .env        # set DB creds
python manage.py migrate
python manage.py runserver
 
