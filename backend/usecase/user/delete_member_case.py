from domain.crud_service import CrudService
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase


class DeleteMemberCaseDto(UseCaseDtoBase):
    db: Session
    org_id: int
    member_id: int

    def __init__(self, db, org_id, user_id):
        self.db = db
        self.org_id = org_id
        self.user_id = user_id


class DeleteMemberCase(UseCaseBase):
    def __init__(self, params: DeleteMemberCaseDto):
        super().__init__(params)

    def execute(self):
        crud_service = CrudService(self.params.db)
        member = crud_service.get_member(org_id=self.params.org_id, user_id=self.params.user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found",
            )
        crud_service.delete_member(member_id=member.id)
        return None



