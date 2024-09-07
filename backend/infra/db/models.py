from typing import List
from sqlalchemy import Integer, String, ForeignKey, BigInteger, JSON, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[BigInteger] = mapped_column(BigInteger, nullable=True, default=func.extract('epoch', func.now()))
    updated_at: Mapped[BigInteger] = mapped_column(BigInteger, nullable=True, default=func.extract('epoch', func.now()), onupdate=func.extract('epoch', func.now()))


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    personal: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    settings: Mapped[dict] = mapped_column(JSON, nullable=True, default={})

    members: Mapped[List["Member"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    roles: Mapped[List["Role"]] = relationship(back_populates="organization", cascade="all, delete-orphan")


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    profile: Mapped[dict] = mapped_column(JSON, nullable=False, default={})
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    settings: Mapped[dict] = mapped_column(JSON, nullable=True, default={})

    memberships: Mapped[List["Member"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    organization: Mapped["Organization"] = relationship(back_populates="roles")

    members: Mapped[list["Member"]] = relationship("Member", back_populates="role", cascade="all, delete-orphan")


class Member(BaseModel):
    __tablename__ = "members"

    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    settings: Mapped[dict] = mapped_column(JSON, nullable=True, default={})

    organization: Mapped["Organization"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="memberships")
    role: Mapped["Role"] = relationship(back_populates="members")
