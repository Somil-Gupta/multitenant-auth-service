from pydantic import BaseModel
class Role_Count(BaseModel):
    role_id: int
    role_name: str
    member_count: int

class Org_Count(BaseModel):
    org_id: int
    org_name: str
    member_count: int


class Org_Role_Count(BaseModel):
    org_id: int
    org_name: str
    role_id: int
    role_name: str
    member_count: int