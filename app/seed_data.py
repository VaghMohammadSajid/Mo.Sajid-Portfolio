# seed_data.py
from app.database import SessionLocal
from app import crud, schemas


def seed_projects():
    db = SessionLocal()
    try:
        # ---- First Project ----
        project1_languages = ["Python"]
        project1_frameworks = ["Django", "Django Oscar", "Django Rest Framework"]
        project1_tools = ["Swagger", "Git", "PycharmIDE"]
        project1_databases = ["PostgreSQL"]
        project1 = schemas.ProjectCreate(
            project_name="E-Commerce Website - OneUpBrand",
            description=[
                "OneUp Brand is a comprehensive e-commerce platform..."
            ],
            my_roll_obj=schemas.MyRollBase(
                roll_title="I contributed as a Full-Stack Developer with the following responsibilities:",
                roll_topic=[
                    "Developed RESTFul APIs using Django Rest Framework...",
                    "Implemented and customized the admin panel...",
                    "Designed and styled the admin interface...",
                    "Collaborated with team members..."
                ]
            ),
            req_skill_obj=schemas.ReqSkillBase(
                language=", ".join(project1_languages),
                frameworks=", ".join(project1_frameworks),
                tools=", ".join(project1_tools),
                database=", ".join(project1_databases)
            ),
            key_achievement=[
                "Successfully developed and deployed scalable APIs...",
                "Customized Django Oscar to meet specific requirements...",
                "Enhanced admin panel usability...",
                "Collaborated with cross-functional team..."
            ],
            img="images/project/oneup.svg",
            logo_img="images/project/oneup.svg",
            github_link="https://github.com/VaghMohammadSajid/OneupBrand_Project-Admin_panel-",
            website_link="",
            start_date="2024-01-01",
            end_date="2024-10-01"
        )
        crud.create_projects(db=db, projects=project1)

        # ---- Second Project ----
        project2_languages = ["Python"]
        project2_frameworks = ["Django", "Django Rest Framework"]
        project2_tools = ["Swagger", "Git", "PycharmIDE"]
        project2_databases = ["PostgreSQL"]
        project2 = schemas.ProjectCreate(
            project_name="SwaggerAPI - TeensTogather",
            description=[
                "Teens Together is an innovative platform designed for online chatting, fostering safe and interactive communication among teenagers. This project focuses on building a secure and user-friendly environment for real-time interactions, ensuring privacy and user engagement."
            ],
            my_roll_obj=schemas.MyRollBase(
                roll_title="I contributed as a API and Backend Developer:",
                roll_topic=[
                    "As a Backend Developer, I was responsible for creating robust APIs using Django Rest Framework (DRF). My work included API development for user authentication, real-time messaging, and user profile management, as well as database design and integration with the frontend team."
                ]
            ),

            req_skill_obj=schemas.ReqSkillBase(
                language=", ".join(project2_languages),
                frameworks=", ".join(project2_frameworks),
                tools=", ".join(project2_tools),
                database=", ".join(project2_databases)
            ),
            key_achievement=[
                "Designed and implemented scalable APIs for real-time communication.",
                "Collaborated effectively with the frontend team to deliver a seamless user experience.",
                "Enhanced data security and privacy by implementing secure authentication mechanisms."
                "Provided comprehensive API documentation for future developers."
            ],
            img="images/project/teens.svg",
            logo_img="images/project/teens.svg",
            github_link="https://github.com/VaghMohammadSajid/teens_togather",
            website_link="",
            start_date="2024-07-01",
            end_date="2025-03-31"
        )
        crud.create_projects(db=db, projects=project2)
    finally:
        db.close()


if __name__ == "__main__":
    seed_projects()
