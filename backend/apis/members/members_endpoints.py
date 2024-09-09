from typing import Annotated

from apis.members import members_schemas
from domain.auth_service import get_current_active_user
from fastapi import APIRouter, Depends, status
from infra.db import models
from infra.db.database import get_db
from sqlalchemy.orm import Session
from usecase.user.delete_member_case import DeleteMemberCase, DeleteMemberCaseDto
from usecase.user.update_member_role_case import UpdateMemberRoleCase, UpdateMemberRoleCaseDto
from usecase.user.invite_member_case import InviteMemberCase, InviteMemberCaseDto

router = APIRouter(tags=["member"])

@router.delete("/organization/{org_id}/member/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    org_id: int,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):
    dto = DeleteMemberCaseDto(db, org_id, user_id)
    return DeleteMemberCase(dto).execute()


@router.patch("/organization/{org_id}/member/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_member_role(
    org_id: int,
    user_id: int,
    role: members_schemas.UpdateRoleRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):
    dto = UpdateMemberRoleCaseDto(db, org_id, user_id, role.role_id)
    return UpdateMemberRoleCase(dto).execute()


@router.post("/organziation/{org_id}/member", status_code=status.HTTP_201_CREATED)
def invite_member(
    org_id: int,
    invite: members_schemas.InviteUserRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[models.User, Depends(get_current_active_user)],
):
    dto = InviteMemberCaseDto(db, org_id, invite.email, invite.role)
    InviteMemberCase(dto).execute()
    return {"message": f"Member created. Invite Link sent at {invite.email}"}
