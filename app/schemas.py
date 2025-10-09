from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import date

# ---------------- MyRoll ----------------
class MyRollBase(BaseModel):
    roll_title: str
    roll_topic: Any  # JSON field

    model_config = {
        "from_attributes": True
    }

class MyRoll(MyRollBase):
    roll_id: int

    class Config:
        from_attributes = True

# ---------------- ReqSkill ----------------
class ReqSkillBase(BaseModel):
    language: str
    frameworks: str
    tools: str
    database: str

    model_config = {
        "from_attributes": True
    }

class ReqSkill(ReqSkillBase):
    req_skill_id: int

    class Config:
        from_attributes = True

# ---------------- Project ----------------
class ProjectBase(BaseModel):
    project_name: str
    description: Any
    key_achievement: Any
    img: Optional[str] = None
    logo_img: Optional[str] = None
    project_video: Optional[str] = None
    github_link: Optional[str] = None
    website_link: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    model_config = {
        "from_attributes": True
    }

# For creating a project (nested objects allowed, no IDs required)
class ProjectCreate(ProjectBase):
    my_roll_obj: MyRollBase
    req_skill_obj: ReqSkillBase

# For reading from DB (IDs included, nested response schemas)
class Project(ProjectBase):
    pro_id: int
    my_roll_obj: MyRoll
    req_skill_obj: ReqSkill

    class Config:
        orm_mode = True
