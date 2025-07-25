from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import jwt
from fastapi import HTTPException, status
from .schema import User, TokenData
import os

class AuthService:
    def __init__(self):
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.ALGORITHM = os.getenv('ALGORITHM')
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

    def authenticate_user(self, db: Session, email: str, password: str) -> User | None:
        try:
            result = db.execute(
                text("EXEC IngresarAlSistema :EmailInstitucional, :Contrasena"),
                {"EmailInstitucional": email, "Contrasena": password}
            )
            row = result.fetchone()
            if row:
                return User(email=row.EmailInstitucional, role=row.idRol)
            return None
        except Exception as e:
            raise e

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("sub")
            role: int = payload.get("role")
            if email is None or role is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
            return TokenData(email=email, role=role)
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )