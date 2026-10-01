import uuid
from typing import Any
import random

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Student, StudentCreate, StudentPublic, StudentsPublic, StudentUpdate, Message, Classe, School

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=StudentPublic)
def create_student(*, session: SessionDep, current_user: CurrentUser, classe_id: uuid.UUID , student_in: StudentCreate
) -> Any:
    """
    Create new student.
    """
    student = Student.model_validate(student_in, update={"classe_id": classe_id})
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@router.get("/", response_model=StudentsPublic)
def read_students(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve students.
    """
    les_classes = [
        uuid.UUID("2a4532d6-7e5d-40fe-876f-f326fb466bfa"),
        uuid.UUID("5fbd8f81-7786-4843-a792-ff57e5d5f0d4"),
        uuid.UUID("3c6cf9d9-b9de-4e62-aade-214eb5fd076a"),
        uuid.UUID("743ef96d-c0e9-4e50-bb4a-424c1aafa67d")
    ]
    valeur_aleatoire = random.choice(les_classes)
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Student)
        count = session.exec(count_statement).one()
        statement = (
            select(Student).order_by(col(Student.created_at).desc()).offset(skip).limit(limit)
        )
        students = session.exec(statement).all()
    else:
        school = session.exec(select(School).where(col(School.responsable_id)==current_user.id)).first() 
        print({"Ecole": school})
        stmt = (
            select(Classe).order_by(col(Classe.created_at).asc()).where(col(Classe.school_id)==school.id)
        )
        classes = session.exec(stmt).all()

        count_statement = (
            select(func.count())
            .select_from(Student)
            # .where(Student.classe_id == classes[0].id)
        )
        count = session.exec(count_statement).one()

        print(f"\nClasse : {classes[0].name}-{school.name}-{school.responsable.full_name}")
        print("-" * 30)
        statement = (
            select(Student)
            # .where(Student.classe_id == classes[0].id)
            .order_by(col(Student.classe_id).asc(), col(Student.nom).asc(), col(Student.prenom).asc())
            .offset(skip)
            .limit(limit)
        )
        students = session.exec(statement).all()
        print({"classe": classes[0].slug, "ecole": classes[0].ecole.name, "responsable": classes[0].ecole.responsable.full_name})
        print({"Mes classe": classes})
                
 
    students_public = [StudentPublic.model_validate(student) for student in students]
    return StudentsPublic(count=count, data=students_public)



@router.get("/{id}", response_model=StudentPublic)
def read_student(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get student by ID.
    """
    student = session.get(Student, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not current_user.is_superuser and (student.classe.ecole.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return student


@router.put("/{id}", response_model=StudentPublic)
def update_student(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    student_in: StudentUpdate,
) -> Any:
    """
    Update a student.
    """
    student = session.get(Student, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not current_user.is_superuser and (student.classe.ecole.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = student_in.model_dump(exclude_unset=True)
    student.sqlmodel_update(update_dict)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@router.delete("/{id}")
def delete_student(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a student.
    """
    student = session.get(Student, id)
    if not studenr:
        raise HTTPException(status_code=404, detail="Student not found")
    if not current_user.is_superuser and (student.classe.ecole.responsable_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(student)
    session.commit()
    return Message(message="Student deleted successfully")
