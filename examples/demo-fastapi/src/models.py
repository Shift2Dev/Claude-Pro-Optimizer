from pydantic import BaseModel, EmailStr
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


# ── SQLAlchemy ORM models ─────────────────────────────────────────────────────

class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)

    items: Mapped[list["ItemDB"]] = relationship("ItemDB", back_populates="owner", cascade="all, delete")


class ItemDB(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(500), default="")
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped[UserDB] = relationship("UserDB", back_populates="items")


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}


class ItemBase(BaseModel):
    title: str
    description: str = ""
    owner_id: int


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    model_config = {"from_attributes": True}
