import uuid
from datetime import UTC, datetime

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list[Item] = Relationship(back_populates="owner", cascade_delete=True)
    schools: list[School] = Relationship(back_populates="responsable", cascade_delete=True)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# ----------------School-----------------------------------
# shared proprieties
class SchoolBase(SQLModel):
    name: str = Field(min_length=3, max_length=80)
    slug: str = Field(min_length=3, max_length=120)
    academie: str = Field(max_length=50, default="Ziguinchor")
    ief: str = Field(max_length=50, default="Bignona")
    directeur: str | None = Field(default=None, max_length=60)
    adresse: str | None = Field(default=None, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=21)

class SchoolCreate(SchoolBase):
    pass


# Properties to receive on item update
class SchoolUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    academie: str | None = Field(default=None, max_length=50)
    ief: str | None = Field(default=None, max_length=50)
    directeur: str | None = Field(default=None, max_length=60)
    adresse: str | None = Field(default=None, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=21)


# Database model, database table inferred from class name
class School(SchoolBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    responsable_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    responsable: User | None = Relationship(back_populates="schools")
    classes: list[Classe] = Relationship(back_populates="ecole", cascade_delete=True)

 
# Properties to return via API, id is always required
class SchoolPublic(SchoolBase):
    id: uuid.UUID
    responsable_id: uuid.UUID
    created_at: datetime | None = None


class SchoolsPublic(SQLModel):
    data: list[SchoolPublic]
    count: int


class ClasseBase(SQLModel):
    name: str = Field(min_length=2, max_length=20)
    slug: str = Field(max_length=25)

class ClasseCreate(ClasseBase):
    pass

class ClasseUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=20)
    slug: str | None = Field(default=None, max_length=25)

class Classe(ClasseBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    school_id: uuid.UUID = Field(
        foreign_key="school.id", nullable=False, ondelete="CASCADE"
    )
    ecole: School | None = Relationship(back_populates="classes")
    eleves: list[Student] = Relationship(back_populates="classe", cascade_delete=True)
    students: list[Cemas] = Relationship(back_populates="laclasse", cascade_delete=True)
    
class ClassePublic(ClasseBase):
    id: uuid.UUID
    school_id: uuid.UUID
    created_at: datetime | None = None
    ecole: School


class ClassesPublic(SQLModel):
    data: list[ClassePublic]
    count: int

# ---------------- Students -----------------
class CemasBase(SQLModel):
    ien: str = Field(min_length=6, max_length=10)
    prenom: str = Field(max_length=35)
    nom: str = Field(max_length=35)
    datnais: str = Field(max_length=50, default=None)
    lieunais: str = Field(max_length=50, default=None)
    sexe: str = Field(max_length=1, default="H")
    pere: str | None = Field(default=None, max_length=60)
    mere: str | None = Field(default=None, max_length=60)
    adresse: str | None = Field(default=None, max_length=120)
    contact: str | None = Field(default=None, max_length=60)


class CemasCreate(CemasBase):
    pass

class CemasUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=20)
    prenom: str | None = Field(default=None, max_length=35)
    nom: str | None = Field(default=None, max_length=35)
    datnais: datetime | None
    lieunais: str | None = Field(default=None, max_length=50)
    sexe: str | None = Field(default=None, max_length=1)
    pere: str | None = Field(default=None, max_length=60)
    mere: str | None = Field(default=None, max_length=60)
    adresse: str | None = Field(default=None, max_length=120)
    contact: str | None = Field(default=None, max_length=60)


class Cemas(CemasBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    classe_id: uuid.UUID = Field(
        foreign_key="classe.id", nullable=False, ondelete="CASCADE"
    )
    laclasse: Classe = Relationship(back_populates="students")

class CemasPublic(CemasBase):
    id: uuid.UUID
    classe_id: uuid.UUID
    created_at: datetime | None = None
    laclasse: Classe


class CemassPublic(SQLModel):
    data: list[CemasPublic]
    count: int


#-----------------------------------------------------------------   
class StudentBase(SQLModel):
    ien: str = Field(min_length=6, max_length=10)
    prenom: str = Field(max_length=35)
    nom: str = Field(max_length=35)
    datnais: str = Field(max_length=50, default=None)
    lieunais: str = Field(max_length=50, default=None)
    sexe: str = Field(max_length=1, default="H")
    pere: str | None = Field(default=None, max_length=60)
    mere: str | None = Field(default=None, max_length=60)
    adresse: str | None = Field(default=None, max_length=120)
    contact: str | None = Field(default=None, max_length=60)



class StudentCreate(StudentBase):
    pass

class StudentUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=20)
    prenom: str | None = Field(default=None, max_length=35)
    nom: str | None = Field(default=None, max_length=35)
    datnais: datetime | None
    lieunais: str | None = Field(default=None, max_length=50)
    sexe: str | None = Field(default=None, max_length=1)
    pere: str | None = Field(default=None, max_length=60)
    mere: str | None = Field(default=None, max_length=60)
    adresse: str | None = Field(default=None, max_length=120)
    contact: str | None = Field(default=None, max_length=60)


class Student(StudentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    classe_id: uuid.UUID = Field(
        foreign_key="classe.id", nullable=False, ondelete="CASCADE"
    )
    classe: Classe = Relationship(back_populates="eleves")
    

class StudentPublic(StudentBase):
    id: uuid.UUID
    classe_id: uuid.UUID
    created_at: datetime | None = None
    classe: Classe


class StudentsPublic(SQLModel):
    count: int
    data: list[StudentPublic]

#------------------- FIN Student ----------

# ------------------ FIN School ---------------------------------


# Shared properties for ITEMS
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
