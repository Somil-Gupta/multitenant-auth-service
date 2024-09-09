import stat
from typing import Annotated

from apis.user import user_schemas
from domain.auth_service import get_current_active_user, get_current_user
from domain.crud_service import CrudService
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from infra.db import models
from infra.db.database import get_db
from sqlalchemy.orm import Session
from usecase.user.create_user_case import CreateUserCase, CreateUserCaseDto
from usecase.user.reset_password_case import ResetPasswordCase, ResetPasswordCaseDto
from usecase.user.signin_user_case import SignInUserCase, SignInUserCaseDto
from usecase.user.create_organization_case import CreateOrgCase, CreateOrgCaseDto


router = APIRouter(tags=["user"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(
    user: user_schemas.UserCreateRequest,
    org: user_schemas.OrganisationCreateRequest,
    db: Session = Depends(get_db),
):
    dto = CreateUserCaseDto(db, user, org)
    CreateUserCase(dto).execute()
    return {"message": "User created and Organization. Please Verify the email to activate the account."}


@router.post(
    "/signin", response_model=user_schemas.Token, status_code=status.HTTP_200_OK
)
def signin(
    # user: Annotated[OAuth2PasswordRequestForm, Depends()],
    user: user_schemas.UserSignInRequest,
    db: Session = Depends(get_db),
):
    dto = SignInUserCaseDto(db, user.email, user.password)
    return SignInUserCase(dto).execute()


@router.patch("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(
    password: user_schemas.UserResetPasswordRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):
    dto = ResetPasswordCaseDto(db, user, password)
    return ResetPasswordCase(dto).execute()

@router.get("/invite-verify", status_code=status.HTTP_200_OK)
def update_status(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_user)],
):
    crud_service = CrudService(db)
    crud_service.update_status(user.id, 1)
    return {"message": f"User {user.email} is now Verified"}

@router.post("/organzation", status_code=status.HTTP_201_CREATED)
def create_organization(
    org: user_schemas.OrganisationCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_user)],
):
    dto = CreateOrgCaseDto(db, user=user, org=org)
    CreateOrgCase(dto).execute()
    return {"message": f"New Organization {org.name} with {user.email} as an admin"}