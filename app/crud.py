from sqlalchemy.orm import Session
from app import schemas, models
from app.models import Projects, ProjectImage, ReqSkill, MyRoll


# ---------------------------
#       PROJECTS
# ---------------------------

def get_projects(db: Session):
    """Return all projects."""
    return db.query(Projects).order_by(Projects.pro_id.desc()).all()


def get_projects_by_id(db: Session, pro_id: int):
    """Return by id projects."""
    return db.query(Projects).filter(Projects.pro_id == pro_id).first()


def get_project_by_name(db: Session, name: str):
    """Fetch a project by name."""
    return db.query(Projects).filter(Projects.project_name == name).first()


def create_or_update_project(db: Session, project: schemas.ProjectCreate):
    # MyRoll
    my_roll = get_or_create_my_roll(db, project.my_roll_obj)

    # ReqSkill
    req_skill = get_or_create_req_skill(db, project.req_skill_obj)

    # Check existing project
    existing = get_project_by_name(db, project.project_name)

    if existing:
        #  UPDATE
        for field, value in project.model_dump(
                exclude={"my_roll_obj", "req_skill_obj", "images"}
        ).items():
            setattr(existing, field, value)

        existing.my_roll_id = my_roll.roll_id
        existing.req_skill_id = req_skill.req_skill_id

        # UPDATE IMAGES
        existing.images.clear()
        for img_path in project.images:
            img = models.ProjectImage(image_path=img_path)
            existing.images.append(img)

        db.commit()
        db.refresh(existing)
        return existing

    else:
        # CREATE
        new_proj = models.Projects(
            **project.model_dump(
                exclude={"my_roll_obj", "req_skill_obj", "images"}
            ),
            my_roll_id=my_roll.roll_id,
            req_skill_id=req_skill.req_skill_id,
        )

        # ADD IMAGES
        for img_path in project.images:
            img = models.ProjectImage(image_path=img_path)
            new_proj.images.append(img)

        db.add(new_proj)
        db.commit()
        db.refresh(new_proj)
        return new_proj


def sync_projects_with_seed(db: Session, seed_projects: list[schemas.ProjectCreate]):
    """
    Synchronize database with seed projects:
    - Create new projects
    - Update existing ones
    - Delete projects missing in seed
    """
    existing_projects = {p.project_name: p for p in db.query(Projects).all()}
    seed_names = {proj.project_name for proj in seed_projects}

    # Create or update
    for proj in seed_projects:
        create_or_update_project(db, proj)

    # Delete removed projects
    for name, project in existing_projects.items():
        if name not in seed_names:
            db.delete(project)
    db.commit()


# ---------------------------
#       MyRoll
# ---------------------------

def get_or_create_my_roll(db: Session, roll_data: schemas.MyRollBase):
    """
    Get or create a MyRoll entry.
    Updates roll_topic if MyRoll exists.
    """
    obj = db.query(MyRoll).filter_by(roll_title=roll_data.roll_title).first()
    if obj:
        obj.roll_topic = roll_data.roll_topic
        db.commit()
        db.refresh(obj)
        return obj

    new_obj = MyRoll(**roll_data.model_dump())
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


# ---------------------------
#       ReqSkill
# ---------------------------

def get_or_create_req_skill(db: Session, skill_data: schemas.ReqSkillBase):
    """
    Get or create a ReqSkill entry.
    """
    obj = db.query(ReqSkill).filter_by(
        language=skill_data.language,
        frameworks=skill_data.frameworks,
        tools=skill_data.tools,
        database=skill_data.database
    ).first()
    if obj:
        return obj

    new_obj = ReqSkill(**skill_data.model_dump())
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


# ---------------------------
#       Delete Projects Api
# ---------------------------

def delete_project(db: Session, pro_id: int) -> bool:
    """
    Delete a project by its ID.
    Returns True if deleted, False if not found.
    """
    project = db.query(Projects).filter(Projects.pro_id == pro_id).first()
    if not project:
        return False

    db.delete(project)
    db.commit()
    return True
