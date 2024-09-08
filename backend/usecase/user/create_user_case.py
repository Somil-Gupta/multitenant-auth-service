from infra.db import models
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from utils.password import get_password_hash
from domain.crud_service import CrudService

class CreateUserCaseDto(UseCaseDtoBase):
    def __init__(self, db, user, org):
        self.db = db
        self.user = user
        self.org = org


class CreateUserCase(UseCaseBase):
    def __init__(self, params: CreateUserCaseDto):
        super().__init__(params)

    def execute(self):
        user_params = self.params.user
        org_params = self.params.org

        db_user = models.User(
            email=user_params.email,
            password=user_params.password,
            profile=user_params.profile,
            status=user_params.status,
            settings=user_params.settings,
        )

        db_org = models.Organization(
            name=org_params.name,
            status=org_params.status,
            personal=org_params.personal,
            settings=org_params.settings,
        )

        user_service = CrudService(self.params.db)
        user = user_service.create_user(db_user)
        org = user_service.create_organization(db_org)
        role = user_service.get_role_by_name("owner")
        db_member = models.Member(
            org_id=org.id,
            user_id=user.id,
            role_id=role.id, #type: ignore
            status=0,
            settings={},
        )
        _ = user_service.create_member(db_member)





