# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


# ---------- MyRoll ----------
class MyRollBase(BaseModel):
    roll_title: str
    roll_topic: Optional[List[str]] = None

    class Config:
        from_attributes = True


# ---------- ReqSkill ----------
class ReqSkillBase(BaseModel):
    language: str
    frameworks: str
    tools: str
    database: str

    class Config:
        from_attributes = True


# ---------- Project ----------
class ProjectBase(BaseModel):
    project_name: str
    project_nickname: str
    project_type: str
    description: Optional[List[str]] = None
    key_achievement: Optional[List[str]] = None
    images: Optional[List[str]] = None
    logo_img: Optional[str] = None
    main_image: Optional[str] = None
    project_video: Optional[str] = None
    github_link: Optional[str] = None
    website_link: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    my_roll_obj: MyRollBase
    req_skill_obj: ReqSkillBase


class Project(ProjectBase):
    pro_id: int
    my_roll_obj: MyRollBase
    req_skill_obj: ReqSkillBase

    class Config:
        from_attributes = True
