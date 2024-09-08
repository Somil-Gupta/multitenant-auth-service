from domain.auth_service import AuthService
from domain.crud_service import CrudService
from fastapi import HTTPException, status
from infra.db import models
from sqlalchemy.orm import Session
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from utils.password import get_password_hash


class ResetPasswordCaseDto(UseCaseDtoBase):
    db: Session
    user: models.User

    def __init__(self, db, user, password):
        self.db = db
        self.user = user
        self.password = password


class ResetPasswordCase(UseCaseBase):
    def __init__(self, params: ResetPasswordCaseDto):
        super().__init__(params)

    def execute(self):
        auth_service = AuthService(db=self.params.db)
        crud_service = CrudService(self.params.db)
        email = self.params.user.email
        if not auth_service.authenticate_user(email=email, password=self.params.password.old_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate password",
                headers={"WWW-Authenticate": "Bearer"},
        )
        if self.params.password.old_password == self.params.password.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password cannot be the same as the old password",
        )
        if self.params.password.new_password != self.params.password.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and Confirm Password do not match",
        )
        crud_service.update_user_password(email, self.params.password.new_password)
        return None




