from infra.db import models
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from domain.crud_service import CrudService

class RoleWiseCaseDto(UseCaseDtoBase):
    def __init__(self, db, org_id):
        self.db = db
        self.org_id = org_id


class RoleWiseCase(UseCaseBase):
    def __init__(self, params: RoleWiseCaseDto):
        super().__init__(params)

    def execute(self):
        crud_service = CrudService(self.params.db)
        role_count = crud_service.get_role_wise_member_count(self.params.org_id)
        result = []
        for role_id, count in role_count:
            role_name = crud_service.get_role_by_id(role_id).name # type: ignore
            result.append({"role_id": role_id, "role_name": role_name, "member_count": count})
        return result

        







