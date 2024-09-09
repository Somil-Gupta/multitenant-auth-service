from fastapi import HTTPException, status
from usecase.base.usecase_base import UseCaseBase, UseCaseDtoBase
from utils.password import get_password_hash
from domain.auth_service import AuthService
from utils.email import send_login_alert_email


class SignInUserCaseDto(UseCaseDtoBase):
    def __init__(self, db, email, password):
        self.db = db
        self.email = email
        self.password = password


class SignInUserCase(UseCaseBase):
    def __init__(self, params: SignInUserCaseDto):
        super().__init__(params)


    def execute(self):

        auth_service = AuthService(db=self.params.db)
        user = auth_service.authenticate_user(email=self.params.email, password=self.params.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate email or password",
                headers={"WWW-Authenticate": "Bearer"},
        )
        # if user.status == 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="User Email was not verified. Check Verification Link in your email",
        #         headers={"X-Error-Message": "User not verified"},
        # )
        user_data = {"sub": user.email}
        access_token = auth_service.create_access_token(data=user_data)
        refresh_token = auth_service.create_refresh_token(data=user_data)
        token_data =  {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        _ = send_login_alert_email(user.email)
        return token_data


