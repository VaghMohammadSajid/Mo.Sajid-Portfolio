# app/seed_data.py
from app import schemas, crud
from app.models import Projects


def get_seed_projects():
    """Return all portfolio projects (for syncing)."""
    return [
        schemas.ProjectCreate(
            project_name="E-Commerce Website OneUpBrand",
            description=["A feature-rich e-commerce platform with Django Oscar integration."],
            my_roll_obj=schemas.MyRollBase(
                roll_title="Full Stack Developer",
                roll_topic=[
                    "Built REST APIs using Django Rest Framework",
                    "Customized Django Oscar modules",
                    "Integrated admin and user modules"
                ]
            ),
            req_skill_obj=schemas.ReqSkillBase(
                language="Python",
                frameworks="Django, Django Oscar, DRF",
                tools="Swagger, Git, PyCharmIDE",
                database="PostgreSQL"
            ),
            key_achievement=[
                "Scalable API design",
                "Efficient admin customization",
                "Seamless database integration"
            ],
            img="images/project/oneup.svg",
            logo_img="images/project/oneup.svg",
            github_link="https://github.com/VaghMohammadSajid/OneupBrand_Project-Admin_panel-",
            website_link="",
            start_date="2024-01-01",
            end_date="2024-10-01",
        ),
        schemas.ProjectCreate(
            project_name="SwaggerAPI Teens & Togather",
            description=["A secure chat API for teenagers with REST and real-time communication."],
            my_roll_obj=schemas.MyRollBase(
                roll_title="API Developer",
                roll_topic=[
                    "Developed RESTful APIs with DRF",
                    "Integrated user authentication",
                    "Worked on real-time message flow"
                ]
            ),
            req_skill_obj=schemas.ReqSkillBase(
                language="Python",
                frameworks="Django, DRF",
                tools="Swagger, Git, PyCharmIDE",
                database="PostgreSQL"
            ),
            key_achievement=[
                "Built scalable messaging APIs",
                "Improved security and authentication",
                "Collaborated with frontend for seamless UX"
            ],
            img="images/project/teens.svg",
            logo_img="images/project/teens.svg",
            github_link="https://github.com/VaghMohammadSajid/teens_togather",
            website_link="",
            start_date="2024-07-01",
            end_date="2025-03-31",
        ),
        schemas.ProjectCreate(
            project_name="Biometric Attendance System",
            description=["A Django-based attendance app using biometric validation."],
            my_roll_obj=schemas.MyRollBase(
                roll_title="Full Stack Developer",
                roll_topic=[
                    "Built backend modules for attendance tracking",
                    "Integrated biometric authentication",
                    "Created responsive front-end with Bootstrap"
                ]
            ),
            req_skill_obj=schemas.ReqSkillBase(
                language="Python, HTML, CSS, JavaScript",
                frameworks="Django, Bootstrap",
                tools="Git, VS Code, Postman",
                database="PostgreSQL"
            ),
            key_achievement=[
                "Automated attendance management",
                "Implemented secure user roles",
                "Deployed real-time attendance reports"
            ],
            img="images/project/biometric-attendance.svg",
            logo_img="images/project/biometric-attendance.svg",
            github_link="https://github.com/VaghMohammadSajid/biometric_attendance",
            website_link="",
            start_date="2024-02-25",
            end_date="2025-03-31",
        ),
    ]


# app/seed_data.py

def seed_all_data(db):
    """
    Sync database with seed data.
    """
    seed_projects = get_seed_projects()

    existing_projects = {p.project_name: p for p in db.query(Projects).all()}
    seed_project_names = [p.project_name for p in seed_projects]

    # Create or update
    for project in seed_projects:
        crud.create_or_update_project(db, project)  # ✅ updated line
        print("------------------------------------------------------------")
        print("✅ Created or Updated!")
        print("------------------------------------------------------------")

    # Delete projects not in seed data
    for name, project in existing_projects.items():
        if name not in seed_project_names:
            db.delete(project)
            print("------------------------------------------------------------")
            print("✅ Deleted!")
            print("------------------------------------------------------------")

    db.commit()
    print("✅ Database synced with seed_data successfully!")
