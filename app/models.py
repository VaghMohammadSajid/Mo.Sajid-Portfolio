# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from app.database import Base


class MyRoll(Base):
    __tablename__ = "my_roll"

    roll_id = Column(Integer, primary_key=True, index=True)
    roll_title = Column(String, nullable=False)
    roll_topic = Column(JSON, nullable=True)

    # Relationship → Projects
    projects = relationship("Projects", back_populates="my_roll_obj")


class ReqSkill(Base):
    __tablename__ = "req_skills"

    req_skill_id = Column(Integer, primary_key=True, index=True)
    language = Column(String, index=True)
    frameworks = Column(String, index=True)
    tools = Column(String, index=True)
    database = Column(String, index=True)

    # One-to-One with Projects
    project = relationship("Projects", back_populates="req_skill_obj", uselist=False)


project_image_association = Table(
    "project_image_association",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.pro_id"), primary_key=True),
    Column("image_id", Integer, ForeignKey("project_images.image_id"), primary_key=True),
)


class ProjectImage(Base):
    __tablename__ = "project_images"

    image_id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)


class Projects(Base):
    __tablename__ = "projects"

    pro_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, unique=True, nullable=False)
    project_nickname = Column(String, nullable=True)
    description = Column(JSON, nullable=True)

    my_roll_id = Column(Integer, ForeignKey("my_roll.roll_id"), nullable=False)
    req_skill_id = Column(Integer, ForeignKey("req_skills.req_skill_id"), nullable=False, unique=True)

    key_achievement = Column(JSON)
    logo_img = Column(String, nullable=True)
    project_video = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    website_link = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    my_roll_obj = relationship("MyRoll", back_populates="projects")
    req_skill_obj = relationship("ReqSkill", back_populates="project")

    main_image = Column(String, nullable=True)

    images = relationship(
        "ProjectImage",
        secondary=project_image_association,
        backref="projects"
    )
