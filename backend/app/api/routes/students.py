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
        "2ca38955-1375-4f48-9d0f-5776d5f35aaa",
        "89bcf47f-c492-4d35-976d-7a5035097b7a",
        "174c812e-2a3f-46ef-94d2-3c56c0cfa1e8",
        "18f98f31-a476-4844-8c98-fd5458b9713f",
        "ba5f3949-1ae7-438a-accd-ba6081488e49",
        "3778ae72-a8dc-4f7e-912e-50c1b49d0c97",
        "c12b5b2d-8b8b-4274-9fbd-8d38d7bca536",
        "e3d13f36-bd71-4331-a639-466801f7abb5",
        "39d4c182-823c-4af2-af40-6b4606efeece",
        "e70b56e4-3115-4898-8e8d-236c0c5e5f86",
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
        # print({"Ecole": school})
        stmt = (
            select(Classe).order_by(col(Classe.created_at).asc()).where(col(Classe.school_id)==school.id)
        )
        classes = session.exec(stmt).all()

        count_statement = (
            select(func.count())
            .select_from(Student)
            .where(Student.classe_id == valeur_aleatoire)
        )
        count = session.exec(count_statement).one()

        # print(f"\nClasse : {classe_slug}-{classe_nom}-{ecole}")
        # print("-" * 30)
        statement = (
            select(Student)
            .where(Student.classe_id == valeur_aleatoire)
            .order_by(col(Student.classe_id).asc(), col(Student.nom).asc(), col(Student.prenom).asc())
            .offset(skip)
            .limit(limit)
        )
        students = session.exec(statement).all()
        # print({"classe": classe.slug, "ecole": classe.ecole.name, "responsable": classe.ecole.responsable.full_name})
        # print({"Mes classe": classes})
                
 
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
