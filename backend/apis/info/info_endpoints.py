from typing import Annotated, List, Sequence

from apis.info import info_schemas
from domain.auth_service import get_current_active_user, get_current_admin_user
from domain.crud_service import CrudService
from fastapi import APIRouter, Depends, status
from infra.db import models
from infra.db.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=["info"])


@router.get("/organization") #, response_model=Sequence[info_schemas.organization])
def organization_list(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):
    crud_service = CrudService(db=db)
    return crud_service.get_org_list()

@router.get("/organization/{org_id}/member")
def org_member_list(
    org_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_admin_user)],
):
    crud_service = CrudService(db=db)
    return crud_service.get_org_members(org_id)

@router.get("/roles")
def roles_list(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):
    crud_service = CrudService(db=db)
    return crud_service.get_role_list()


