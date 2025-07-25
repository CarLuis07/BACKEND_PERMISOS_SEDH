from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from .controller import AuthController
from .schema import Token, TokenData, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
auth_controller = AuthController()

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    return await auth_controller.verify_current_user(token)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user_login = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_controller.login_user(db, user_login)