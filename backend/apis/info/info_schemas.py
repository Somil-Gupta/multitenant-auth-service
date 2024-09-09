from pydantic import BaseModel, ConfigDict, EmailStr, Field

class InviteUserRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user to be invited")
    role: str = Field(default="member", description="Role for the invited user")
    model_config = ConfigDict(from_attributes=True, extra="ignore")

class UpdateRoleRequest(BaseModel):
    role_id: int = Field(..., description="Role id of the role to be updated to")

class InfoBaseModel(BaseModel):
    id: int 
    created_at: int
    updated_at: int

class Role(InfoBaseModel):
    name: str
    description: str | None

# class Organization(InfoBaseModel):
#     name: 




