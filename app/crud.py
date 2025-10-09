from sqlalchemy.orm import Session
from app import models, schemas


def get_projects(db: Session):
    return db.query(models.Projects).all()


def create_projects(db: Session, projects: schemas.ProjectCreate):
    existing = db.query(models.Projects).filter_by(project_name=projects.project_name).first()
    if existing:
        existing.description = projects.description
        existing.my_roll_id = get_or_create_my_roll(db, projects.my_roll_obj).roll_id
        existing.req_skill_id = get_or_create_req_skill(db, projects.req_skill_obj).req_skill_id
        existing.key_achievement = projects.key_achievement
        existing.img = projects.img
        existing.logo_img = projects.logo_img
        existing.github_link = projects.github_link
        existing.website_link = projects.website_link
        existing.start_date = projects.start_date
        existing.end_date = projects.end_date
        db.commit()
        db.refresh(existing)
        return existing
    else:
        my_roll = get_or_create_my_roll(db, projects.my_roll_obj)
        req_skill = get_or_create_req_skill(db, projects.req_skill_obj)
        new_project = models.Projects(
            project_name=projects.project_name,
            description=projects.description,
            my_roll_id=my_roll.roll_id,
            req_skill_id=req_skill.req_skill_id,
            key_achievement=projects.key_achievement,
            img=projects.img,
            logo_img=projects.logo_img,
            github_link=projects.github_link,
            website_link=projects.website_link,
            start_date=projects.start_date,
            end_date=projects.end_date
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project


# Make sure these functions exist in crud.py
def get_or_create_my_roll(db: Session, my_roll_obj: schemas.MyRollBase):
    obj = db.query(models.MyRoll).filter_by(roll_title=my_roll_obj.roll_title).first()
    if obj:
        return obj
    new_obj = models.MyRoll(
        roll_title=my_roll_obj.roll_title,
        roll_topic=my_roll_obj.roll_topic
    )
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


def get_or_create_req_skill(db: Session, req_skill_obj: schemas.ReqSkillBase):
    obj = db.query(models.ReqSkill).filter_by(
        language=req_skill_obj.language,
        frameworks=req_skill_obj.frameworks,
        tools=req_skill_obj.tools,
        database=req_skill_obj.database
    ).first()
    if obj:
        return obj
    new_obj = models.ReqSkill(
        language=req_skill_obj.language,
        frameworks=req_skill_obj.frameworks,
        tools=req_skill_obj.tools,
        database=req_skill_obj.database
    )
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj
