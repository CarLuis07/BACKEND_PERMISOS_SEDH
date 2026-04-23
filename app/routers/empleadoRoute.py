from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.empleadoSchema import Empleado as EmpleadoSchema
from app.schemas.empleadoSchema import EmpleadoCreate, EmpleadoDetalle, EmpleadoEmailRequest, EmpleadoUpdate
from app.controllers.empleadoController import obtener_empleado_por_email, crear_empleado, actualizar_empleado
from app.routers.authRoute import get_current_active_user_with_role
from app.schemas.authSchema import TokenData

router = APIRouter()

@router.post("/empleados/buscar", response_model=EmpleadoDetalle)
async def buscar_empleado_por_email(
    request: EmpleadoEmailRequest,
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_active_user_with_role(5))
):
    try:
        empleado = obtener_empleado_por_email(db, request.email_institucional)
        if empleado is None:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return empleado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/empleados/", status_code=201)
async def create_empleado(
    empleado: EmpleadoCreate, 
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(5))
):
    try:
        return crear_empleado(db, current_user.email, empleado.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/empleados/actualizar", status_code=200)
async def update_empleado(
    empleado: EmpleadoUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(5))
):
    try:
        return actualizar_empleado(db, current_user.email, empleado.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))