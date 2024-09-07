import os
from typing import List

from infra.db import models
from infra.db.database import get_db
from sqlalchemy import func, select, delete, update
from sqlalchemy.orm import Session
from utils.password import get_password_hash



class UserService:
    db: Session
    
    def __init__(self):
        self.db = get_db()

    def create_user(self, user: models.User):
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
    
    def create_organization(self, organization: models.Organization):
        self.db.add(organization)
        self.db.flush()
        self.db.refresh(organization)
        return organization
    
    def create_member(self, member: models.Member):
        self.db.add(member)
        self.db.flush()
        self.db.refresh(member)
        return member
    
    def create_role(self, role: models.Role):
        self.db.add(role)
        self.db.flush()
        self.db.refresh(role)
        return role
    
    def delete_user(self, email: str):
        stmt = delete(models.User).where(models.User.email == email)
        self.db.execute(stmt)
        self.db.commit()

    def reset_password(self, email: str, new_password: str):
        new_hashed_password = get_password_hash(password=new_password)
        stmt = update(models.User).where(models.User.email == email).values(password=new_hashed_password)
        self.db.execute(stmt)
        self.db.commit()

    def update_role(self, user_id: int, new_role_id: int):
        stmt = update(models.Member).where(models.Member.user_id == user_id).values(role_id=new_role_id)
        self.db.execute(stmt)
        self.db.commit()

    def update_status(self, user_id: int, new_status: int):
        stmt = update(models.User).where(models.User.id == user_id).values(status=new_status)
        self.db.execute(stmt)
        self.db.commit()

        
    

    
    

    

