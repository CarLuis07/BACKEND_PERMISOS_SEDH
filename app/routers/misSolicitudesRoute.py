from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.misSolicitudesSchema import MisSolicitudesEmpleadoCargarDatos, MisSolicitudesEmergenciaEmpleadoCargarDatos
from app.schemas.authSchema import TokenData
from app.controllers.misSolicitudesController import cargar_datos_ver_mis_solicitudes, cargar_datos_ver_mis_solicitudes_emergencia
from app.routers.authRoute import get_current_active_user

router = APIRouter()

@router.get("/misSolicitudes/", response_model=List[MisSolicitudesEmpleadoCargarDatos])
def cargar_mis_solcitudes(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        mi_solictud = cargar_datos_ver_mis_solicitudes(db, current_user)
        if mi_solictud:
            return mi_solictud
        raise HTTPException(status_code=404, detail="Solicitudes no encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/misSolicitudesEmergencia/", response_model=List[MisSolicitudesEmergenciaEmpleadoCargarDatos])
def cargar_mis_solcitudes_emergencia(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        mi_solictud = cargar_datos_ver_mis_solicitudes_emergencia(db, current_user)
        if mi_solictud:
            return mi_solictud
        raise HTTPException(status_code=404, detail="Solicitudes no encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))