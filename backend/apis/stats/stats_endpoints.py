from datetime import datetime
from typing import Annotated, List

from domain.auth_service import get_current_active_user
from domain.crud_service import CrudService
from fastapi import APIRouter, Depends, status
from infra.db import models
from infra.db.database import get_db
from sqlalchemy.orm import Session
from apis.stats.stats_schemas import Role_Count, Org_Count
from usecase.stats.role_wise_case import RoleWiseCase, RoleWiseCaseDto
from usecase.stats.org_wise_case import OrgWiseCase, OrgWiseCaseDto
from usecase.stats.org_wise_role_wise_case import OrgWiseRoleWiseCase, OrgWiseRoleWiseCaseDto

router = APIRouter(tags=["stats"])


@router.get("/role-wise-num-members/{org_id}", response_model=List[Role_Count])
def role_wise_num_members(
    org_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):  
    dto = RoleWiseCaseDto(db, org_id)
    return RoleWiseCase(dto).execute()

@router.get("/org-wise-num-members", response_model=List[Org_Count])
def org_wise_num_members(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
    from_time: datetime | None = None,
    to_time: datetime | None = None,
):  
    dto = OrgWiseCaseDto(db, from_time, to_time)
    return OrgWiseCase(dto).execute()

@router.get("/org-wise-role-wise-num-members")
def org_wise_role_wise_num_members(

    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
    from_time: datetime | None = None,
    to_time: datetime | None = None,
):
    dto = OrgWiseRoleWiseCaseDto(db, from_time=from_time, to_time=to_time)
    return OrgWiseRoleWiseCase(dto).execute()
