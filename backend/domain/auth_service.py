import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer 
from infra.db import models
from infra.db.database import get_db
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.password import verify_password

# Secret key for signing tokens (You should keep this in an environment variable)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440  # 1 day

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/signin")

class AuthService:
    db: Session
    
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        stmt = select(models.User).where(models.User.email == email)
        return self.db.scalars(stmt).first()
    
    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email=email)
        if user and verify_password(password, user.password):
            return user
        return False

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

auth_service = AuthService(get_db()) # type: ignore

async def get_current_user(token): #: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception
    email = payload.get("sub")
    user = auth_service.get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if not current_user.status:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user. Please Verify your details")
    return current_user

async def get_current_admin_user( 
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if not current_user.profile.get("owner"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not an owner")
    return current_user