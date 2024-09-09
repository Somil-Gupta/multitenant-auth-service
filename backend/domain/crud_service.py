from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from infra.db import models
from sqlalchemy import BigInteger, delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from utils.password import get_password_hash
from utils.time import datetime_to_epoch

DEFAULT_ROLES = [
    {"name": "owner", "description": "Administrator role with all permissions."},
    {"name": "member", "description": "General member role with limited permissions."},
]


class CrudService:
    db: Session

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: models.User):
        try:
            user.password = get_password_hash(password=user.password)
            self.db.add(user)
            self.db.flush()
            self.db.refresh(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        return user

    def create_organization(self, organization: models.Organization):
        try:
            self.db.add(organization)
            self.db.flush()
            self.db.refresh(organization)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization with same already exists",
            )
        self.populate_roles(organization.id)
        return organization

    def create_member(self, member: models.Member):
        try:
            self.db.add(member)
            self.db.flush()
            self.db.refresh(member)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Member already exists",
            )
        return member

    def create_role(self, role: models.Role):
        self.db.add(role)
        self.db.flush()
        self.db.refresh(role)

    def delete_user(self, email: str):
        stmt = delete(models.User).where(models.User.email == email)
        self.db.execute(stmt)
        self.db.commit()

    def update_user_password(self, email: str, new_password: str):
        new_hashed_password = get_password_hash(password=new_password)
        stmt = (
            update(models.User)
            .where(models.User.email == email)
            .values(password=new_hashed_password)
        )
        self.db.execute(stmt)
        self.db.commit()

    def update_role(self, member_id: int, new_role_id: int):
        stmt = (
            update(models.Member)
            .where(models.Member.id == member_id)
            .values(role_id=new_role_id)
        )
        self.db.execute(stmt)
        self.db.commit()

    def update_status(self, user_id: int, new_status: int):
        stmt = (
            update(models.User)
            .where(models.User.id == user_id)
            .values(status=new_status)
        )
        self.db.execute(stmt)
        self.db.commit()

    def get_role_by_name(self, name: str):
        stmt = select(models.Role).where(models.Role.name == name)
        return self.db.scalars(stmt).first()

    def get_role_by_id(self, role_id: int):
        stmt = select(models.Role).where(models.Role.id == role_id)
        return self.db.scalars(stmt).first()

    def populate_roles(self, org_id: int):
        for role in DEFAULT_ROLES:
            existing_role = self.get_role_by_name(role["name"])
            if not existing_role:
                role_obj = models.Role(
                    name=role["name"], description=role["description"], org_id=org_id
                )
                self.create_role(role_obj)

    def get_user_by_email(self, email: str):
        stmt = select(models.User).where(models.User.email == email)
        return self.db.scalars(stmt).first()

    def delete_member(self, member_id: int):
        stmt = delete(models.Member).where(models.Member.id == member_id)
        self.db.execute(stmt)
        self.db.commit()

    def get_member(self, org_id: int, user_id: int):
        stmt = (
            select(models.Member)
            .where(models.Member.org_id == org_id)
            .where(models.Member.user_id == user_id)
        )
        return self.db.scalars(stmt).first()

    def get_org_by_id(self, org_id: int):
        stmt = select(models.Organization).where(models.Organization.id == org_id)
        return self.db.scalars(stmt).first()

    # def get_members(self, org_id: int):
    #     stmt = select(models.Member).where(models.Member.org_id == org_id)
    #     return self.db.scalars(stmt).all()

    def get_role_wise_member_count(self, org_id: int):

        stmt = (
            select(models.Member.role_id, func.count(models.Member.id))
            .where(models.Member.org_id == org_id)
            .group_by(models.Member.role_id)
        )
        return self.db.execute(stmt).fetchall()

    def time_filter(
        self, stmt, from_time: Optional[datetime], to_time: Optional[datetime]
    ):
        if from_time:
            from_epoch = datetime_to_epoch(from_time)
            stmt = stmt.where(models.Member.created_at >= from_epoch)
        if to_time:
            to_epoch = datetime_to_epoch(to_time)
            stmt = stmt.where(models.Member.created_at <= to_epoch)
        return stmt

    def get_org_wise_member_count(
        self, from_time: Optional[datetime] = None, to_time: Optional[datetime] = None
    ):
        stmt = select(models.Member.org_id, func.count(models.Member.id)).group_by(
            models.Member.org_id
        )
        stmt = self.time_filter(stmt, from_time, to_time)
        return self.db.execute(stmt).fetchall()

    def get_org_wise_role_wise_member_count(
        self, from_time: Optional[datetime] = None, to_time: Optional[datetime] = None
    ):
        stmt = select(
            models.Member.org_id, models.Member.role_id, func.count(models.Member.id)
        ).group_by(models.Member.org_id, models.Member.role_id)
        stmt = self.time_filter(stmt, from_time, to_time)
        return self.db.execute(stmt).fetchall()

    def get_org_list(self):
        stmt = select(models.Organization)
        return self.db.scalars(stmt).all()

    def get_org_members(self, org_id: int):
        stmt = select(models.Member).where(models.Member.org_id == org_id)
        return self.db.scalars(stmt).all()

    def get_role_list(self, org_id):
        stmt = select(models.Role).where(models.Role.org_id == org_id)
        return self.db.scalars(stmt).all()
