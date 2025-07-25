from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .service import AuthService
from .schema import UserLogin, TokenData
from datetime import timedelta

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    async def login_user(self, db: Session, user_login: UserLogin):
        user = self.auth_service.authenticate_user(db, user_login.email, user_login.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=self.auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.auth_service.create_access_token(
            data={"sub": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def verify_current_user(self, token: str) -> TokenData:
        return self.auth_service.verify_token(token)