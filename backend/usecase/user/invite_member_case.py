from domain.crud_service import CrudService
from fastapi import HTTPException, status
from infra.db import models
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from utils.password import generate_password
from utils.email import send_signup_invite_email, send_org_invite_email


class InviteMemberCaseDto(UseCaseDtoBase):
    def __init__(self, db, org_id, email, role):
        self.db = db
        self.org_id = org_id
        self.email = email
        self.role = role


class InviteMemberCase(UseCaseBase):
    def __init__(self, params: InviteMemberCaseDto):
        super().__init__(params)

    def execute(self):
        crud_service = CrudService(self.params.db)
        org = crud_service.get_org_by_id(org_id=self.params.org_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No organization with given org_id found",
            )

        user = crud_service.get_user_by_email(email=self.params.email)

        if not user:
            generated_password = generate_password()
            db_user = models.User(email=self.params.email, password=generated_password, status=1)
            user = crud_service.create_user(db_user)
            _ = send_signup_invite_email(user.email, generated_password)

        role = crud_service.get_role_by_name(name=self.params.role)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No role {self.params.role} found in db",
            )
        
        db_member = models.Member(
            org_id=self.params.org_id,
            user_id=user.id,
            role_id=role.id,  # type: ignore
            status=0,
            settings={},
        )

        db_member = models.Member(
            org_id=org.id,
            user_id=user.id,
            role_id=role.id,  # type: ignore
            status=0,
            settings={},
        )
        _ = crud_service.create_member(db_member)
        _ = send_org_invite_email(user.email, org.name)
        return None
