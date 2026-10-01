import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Classe, ClasseCreate, ClassePublic, ClassesPublic, ClasseUpdate, Message, School

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("/", response_model=ClassePublic)
def create_classe(
    *, session: SessionDep,current_user: CurrentUser, school_id: uuid.UUID, classe_in: ClasseCreate
) -> Any:
    """
    Create new classe.
    """
    if current_user.is_superuser:
        statement = (
            select(School).where(id==school_id)
        )
        school = session.exec(statement).first()
        print(school)
    else:
        statement = (
            select(School).where(School.responsable_id == current_user.id)
        )
        school = session.exec(statement).first()
        print(school)
        if not school:
            raise HTTPException(status_code=403, detail="Not enough permissions")

    classe = Classe.model_validate(classe_in, update={"school_id": school_id})
    session.add(classe)
    session.commit()
    session.refresh(classe)
    return classe


@router.get("/", response_model=ClassesPublic)
def read_classes(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve classes.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Classe)
        count = session.exec(count_statement).one()
        statement = (
            select(Classe).order_by(col(Classe.school_id).asc(), col(Classe.slug).asc()).offset(skip).limit(limit)
        )
        classes = session.exec(statement).all()
    else:
        stmt = (
            select(School).where(School.responsable_id == current_user.id)
        )
        school = session.exec(stmt).first()
        print({"ecole": school})
        count_statement = (
            select(func.count())
            .select_from(Classe)
            .where(Classe.school_id == school.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Classe)
            .where(Classe.school_id == school.id)
            .order_by(col(Classe.slug).asc())
            .offset(skip)
            .limit(limit)
        )
        classes = session.exec(statement).all()
 
    classes_public = [ClassePublic.model_validate(classe) for classe in classes]
    return ClassesPublic(data=classes_public, count=count)



@router.get("/{id}", response_model=ClassePublic)
def read_classe(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get classe by ID.
    """
    classe = session.get(Classe, id)
    if not classe:
        raise HTTPException(status_code=404, detail="Classe not found")
    if not current_user.is_superuser and (classe.ecole.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return classe


@router.put("/{id}", response_model=ClassePublic)
def update_classe(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    classe_in: ClasseUpdate,
) -> Any:
    """
    Update a classe.
    """
    classe = session.get(Classe, id)
    if not classe:
        raise HTTPException(status_code=404, detail="Classe not found")
    if not current_user.is_superuser and (classe.ecole.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = classe_in.model_dump(exclude_unset=True)
    classe.sqlmodel_update(update_dict)
    session.add(classe)
    session.commit()
    session.refresh(classe)
    return classe


@router.delete("/{id}")
def delete_classe(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a classe.
    """
    classe = session.get(Classe, id)
    if not classe:
        raise HTTPException(status_code=404, detail="Classe not found")
    if not current_user.is_superuser and (classe.ecole.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(classe)
    session.commit()
    return Message(message="Classe deleted successfully")
