from infra.db import models
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from domain.crud_service import CrudService


class OrgWiseRoleWiseCaseDto(UseCaseDtoBase):
    def __init__(self, db, from_time, to_time):
        self.db = db
        self.from_time = from_time
        self.to_time = to_time


class OrgWiseRoleWiseCase(UseCaseBase):
    def __init__(self, params: OrgWiseRoleWiseCaseDto):
        super().__init__(params)

    def execute(self):
        crud_service = CrudService(self.params.db)
        org_count = crud_service.get_org_wise_role_wise_member_count(
            from_time=self.params.from_time, to_time=self.params.to_time
        )
        result = []
        for org_id, role_id, count in org_count:
            org_name = crud_service.get_org_by_id(org_id).name  # type: ignore
            role_name = crud_service.get_role_by_id(role_id).name  # type: ignore
            result.append(
                {
                    "org_id": org_id,
                    "org_name": org_name,
                    "role_id": role_id,
                    "role_name": role_name,
                    "member_count": count,
                }
            )
        return result
