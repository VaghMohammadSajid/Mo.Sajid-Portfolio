# app/seed_data.py
from app import schemas, crud
from app.models import Projects


def get_seed_projects():
    """Return all portfolio projects (for syncing)."""
    return [
        schemas.ProjectCreate(
            project_name="E-Commerce Website OneUpBrand",
            project_nickname="OneUpBrand",
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
            images=[  # ✅ MULTIPLE IMAGES
                "images/project/oneup/dashboard.png",
                "images/project/oneup/dashboard-1.png",
                "images/project/oneup/orders.png",
            ],
            logo_img="images/project/oneup/oneup.svg",
            main_image="images/project/oneup/oneup.svg",
            github_link="https://github.com/VaghMohammadSajid/OneupBrand_Project-Admin_panel-",
            website_link="",
            start_date="2024-01-01",
            end_date="2024-10-01",
        ),
        schemas.ProjectCreate(
            project_name="RoseValley E-commerce Website",
            project_nickname="RoseValley",
            description=[
                "RoseValley is an E-commerce platform developed as a college project using Java, JSP, Servlet, and Hibernate. "
                "It provides a simple and user-friendly online shopping experience with secure authentication, product catalog, "
                "shopping cart, and order management features."
            ],
            my_roll_obj=schemas.MyRollBase(
                roll_title="Full Stack Developer",
                roll_topic=[
                    "Designed and developed both frontend and backend modules",
                    "Implemented user authentication and authorization",
                    "Built product listing, cart, and order management features",
                    "Worked with database integration using Hibernate ORM"
                ]
            ),
            req_skill_obj=schemas.ReqSkillBase(
                language="Java, HTML, CSS, JavaScript",
                frameworks="JSP, Servlet, Hibernate, Bootstrap",
                tools="Git, VS Code, Postman, Apache Tomcat",
                database="MySQL"
            ),
            key_achievement=[
                "Successfully developed a complete end-to-end e-commerce application",
                "Implemented admin panel for product management",
                "Integrated shopping cart and order tracking system",
                "Deployed and tested the application on Apache Tomcat server"
            ],
            images=[
                "images/project/rosevalley/homepage.png",
                "images/project/rosevalley/orderplace.png"
            ],
            logo_img="images/project/rosevalley/rosevalley_logo.svg",
            main_image="images/project/rosevalley/product_image.jpg",
            github_link="https://github.com/VaghMohammadSajid/RoseValley",
            website_link="http://localhost:8080/RoseValley",
            start_date="2024-02-25",
            end_date="2025-03-31",
        ),
        schemas.ProjectCreate(
            project_name="Biometric Attendance System",
            project_nickname="Biometric Attendance",
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
            images=[
                "images/project/biometric-attendance.png"
            ],
            logo_img="images/project/biometric-attendance/biometric_attendance_logo.svg",
            main_image="images/project/biometric-attendance/biometric_attendance_logo.svg",
            github_link="https://github.com/VaghMohammadSajid/RoseVally_E_Commmerce",
            website_link="",
            start_date="2024-02-25",
            end_date="2025-03-31",
        ),
        schemas.ProjectCreate(
            project_name="SwaggerAPI Teens & Togather",
            project_nickname="Teens&Togather",
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
            images=[  # ✅ ONLY THIS
                "images/project/teens/main.png",
                "images/project/teens/appointmeant.png",
                "images/project/teens/doctor.png",
                "images/project/teens/doctor-1.png",
                "images/project/teens/dynamic-content.png",
                "images/project/teens/happy.png",
                "images/project/teens/meditation.png",
                "images/project/teens/user.png",
                "images/project/teens/user-1.png",
                "images/project/teens/user-2.png",
                "images/project/teens/voice-day.png",
            ],
            logo_img="images/project/teens/teens_logo.png",
            main_image="images/project/teens/teens_logo.png",
            github_link="https://github.com/VaghMohammadSajid/teens_togather",
            website_link="",
            start_date="2024-07-01",
            end_date="2025-03-31",
        ),
    ]


# app/seed_data.py

def seed_all_data(db):
    """
    Sync database with seed data.
    """
    seed_projects = get_seed_projects()

    existing_projects = {
        p.project_name: p for p in db.query(Projects).all()
    }

    seed_project_names = [p.project_name for p in seed_projects]

    # Create or update
    for project in seed_projects:
        crud.create_or_update_project(db, project)  # ✅ updated line
        print("------------------------------------------------------------")
        print("✅ Created or Updated!")
        print("✅ Created or Updated:", project.project_name)
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
