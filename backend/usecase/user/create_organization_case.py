from infra.db import models
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from utils.password import get_password_hash
from domain.crud_service import CrudService
from utils.email import send_signup_invite_email, send_org_invite_email

class CreateOrgCaseDto(UseCaseDtoBase):
    def __init__(self, db, user, org):
        self.db = db
        self.user = user
        self.org = org


class CreateOrgCase(UseCaseBase):
    def __init__(self, params: CreateOrgCaseDto):
        super().__init__(params)

    def execute(self):
        org_params = self.params.org

        db_org = models.Organization(
            name=org_params.name,
            status=org_params.status,
            personal=org_params.personal,
            settings=org_params.settings,
        )
        crud_service = CrudService(self.params.db)        
        org = crud_service.create_organization(db_org)
        role = crud_service.get_role_by_name("owner")
        user = self.params.user
        db_member = models.Member(
            org_id=org.id,
            user_id=user.id,
            role_id=role.id, #type: ignore
            status=0,
            settings={},
        )
        _ = crud_service.create_member(db_member)
        _ = send_org_invite_email(user.email, org.name)





