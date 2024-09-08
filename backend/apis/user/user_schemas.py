import time
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreateRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")
    profile: Optional[Dict] = Field(default_factory=dict, description="User profile information in JSON format")
    status: int = Field(0, description="Status of the user", ge=0)
    settings: Optional[Dict] = Field(default_factory=dict, description="Additional settings in JSON format")

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class OrganisationCreateRequest(BaseModel):
    name: str = Field(..., description="Name of the organisation")
    status: int = Field(0, description="Status of the organisation", ge=0)
    personal: Optional[bool] = Field(False, description="Flag indicating if this is a personal organisation")
    settings: Optional[Dict] = Field(default_factory=dict, description="Additional settings in JSON format")

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class UserSignInRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class UserResetPasswordRequest(BaseModel):
    old_password: str = Field(..., description="Old Password of the user")
    new_password: str = Field(..., description="New Password of the user")
    confirm_new_password: str = Field(..., description="Confirm New Password of the user")

    model_config = ConfigDict(from_attributes=True, extra="ignore")