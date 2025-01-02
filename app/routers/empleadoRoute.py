from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.empleadoSchema import Empleado as EmpleadoSchema
from app.controllers.empleadoController import obtener_empleados
from app.routers.authRoute import get_current_active_user_with_role
from app.schemas.authSchema import TokenData

router = APIRouter()

@router.get("/empleados/", response_model=list[EmpleadoSchema])
async def read_empleados(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_active_user_with_role(2))):
    try:
        return obtener_empleados(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))