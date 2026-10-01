import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import School, SchoolCreate, SchoolPublic, SchoolsPublic, SchoolUpdate, Message

router = APIRouter(prefix="/schools", tags=["schools"])


@router.get("/", response_model=SchoolsPublic)
def read_schools(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve schools.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(School)
        count = session.exec(count_statement).one()
        statement = (
            select(School).order_by(col(School.created_at).desc()).offset(skip).limit(limit)
        )
        schools = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(School)
            .where(School.responsable_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(School)
            .where(School.responsable_id == current_user.id)
            .order_by(col(School.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        schools = session.exec(statement).all()

    schools_public = [SchoolPublic.model_validate(school) for school in schools]
    return SchoolsPublic(data=schools_public, count=count)


@router.get("/{id}", response_model=SchoolPublic)
def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get school by ID.
    """
    school = session.get(School, id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    if not current_user.is_superuser and (school.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return school


@router.post("/", response_model=SchoolPublic)
def create_school(
    *, session: SessionDep, current_user: CurrentUser, school_in: SchoolCreate
) -> Any:
    """
    Create new school.
    """
    school = School.model_validate(school_in, update={"responsable_id": current_user.id})
    session.add(school)
    session.commit()
    session.refresh(school)
    return school


@router.put("/{id}", response_model=SchoolPublic)
def update_school(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    school_in: SchoolUpdate,
) -> Any:
    """
    Update a school.
    """
    school = session.get(School, id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    if not current_user.is_superuser and (school.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = school_in.model_dump(exclude_unset=True)
    school.sqlmodel_update(update_dict)
    session.add(school)
    session.commit()
    session.refresh(school)
    return school


@router.delete("/{id}")
def delete_school(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an school.
    """
    school = session.get(school, id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    if not current_user.is_superuser and (school.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(school)
    session.commit()
    return Message(message="School deleted successfully")
