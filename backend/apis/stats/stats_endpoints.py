from datetime import datetime
from typing import Annotated

from domain.auth_service import get_current_active_user, get_current_admin_user
from domain.crud_service import CrudService
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from infra.db import models
from infra.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["stats"])


@router.get("/role-wise-num-members")
def role_wise_num_members(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):
    crud_service = CrudService(db)
    return crud_service.get_role_wise_member_count()

@router.get("/org-wise-num-members")
def org_wise_num_members(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
    from_time: datetime | None = None,
    to_time: datetime | None = None,
):
    crud_service = CrudService(db)
    return crud_service.get_org_wise_member_count(from_time=from_time, to_time=to_time)

@router.get("/org-wise-role-wise-num-members")
def org_wise_role_wise_num_members(

    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
    from_time: datetime | None = None,
    to_time: datetime | None = None,
):
    crud_service = CrudService(db)
    return crud_service.get_org_wise_role_wise_member_count(from_time=from_time, to_time=to_time)

