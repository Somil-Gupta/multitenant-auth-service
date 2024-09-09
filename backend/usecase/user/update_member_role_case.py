from domain.crud_service import CrudService
from fastapi import HTTPException, status
from infra.db import models
from sqlalchemy.orm import Session
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from utils.password import get_password_hash


class UpdateMemberRoleCaseDto(UseCaseDtoBase):
    db: Session
    org_id: int
    member_id: int
    role: str

    def __init__(self, db, org_id, user_id, role_id):
        self.db = db
        self.org_id = org_id
        self.user_id = user_id
        self.role_id = role_id


class UpdateMemberRoleCase(UseCaseBase):
    def __init__(self, params: UpdateMemberRoleCaseDto):
        super().__init__(params)

    def execute(self):
        crud_service = CrudService(self.params.db)
        member = crud_service.get_member(org_id=self.params.org_id, user_id=self.params.user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found",
            )
        role = crud_service.get_role_by_id(role_id=self.params.role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid Role Change requested",
            )
        return crud_service.update_role(member_id=member.id, new_role_id=role.id)



