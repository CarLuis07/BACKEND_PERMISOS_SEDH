from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.empleadoSchema import Empleado as EmpleadoSchema
from app.controllers.empleadoController import obtener_empleados

router = APIRouter()

@router.get("/empleados/", response_model=list[EmpleadoSchema])
def read_empleados(db: Session = Depends(get_db)):
    try:
        return obtener_empleados(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))