from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON


class MyRoll(Base):
    __tablename__ = "my_roll"

    roll_id = Column(Integer, primary_key=True, index=True)
    roll_title = Column(String, index=True)
    roll_topic = Column(JSON)

    project = relationship("Projects", back_populates="my_roll_obj", uselist=False)


class ReqSkill(Base):
    __tablename__ = "req_skills"

    req_skill_id = Column(Integer, primary_key=True, index=True)
    language = Column(String, index=True)
    frameworks = Column(String, index=True)
    tools = Column(String, index=True)
    database = Column(String, index=True)

    project = relationship("Projects", back_populates="req_skill_obj", uselist=False)


class Projects(Base):
    __tablename__ = "projects"

    pro_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    description = Column(JSON)

    my_roll_id = Column(Integer, ForeignKey("my_roll.roll_id"), unique=True)
    req_skill_id = Column(Integer, ForeignKey("req_skills.req_skill_id"), unique=True)

    my_roll_obj = relationship("MyRoll", back_populates="project")
    req_skill_obj = relationship("ReqSkill", back_populates="project")

    key_achievement = Column(JSON)
    img = Column(String, nullable=True)
    logo_img = Column(String, nullable=True)
    project_video = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    website_link = Column(String, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
