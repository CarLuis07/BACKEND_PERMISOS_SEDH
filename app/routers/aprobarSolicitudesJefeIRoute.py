from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.aprobarSoliciitudesJefeISchema import SolicitudesJefeICargarDatos, SolicitudesJefeIResponder
from app.schemas.authSchema import TokenData
from app.controllers.aprobarSolicitudesJefeIController import cargar_datos_aprobar_solicitudes_jefeI, responder_permiso
from app.routers.authRoute import get_current_active_user_with_rol

router = APIRouter()

@router.get("/aprobarSolicitudes/", response_model=List[SolicitudesJefeICargarDatos])
def cargar_solicitudes(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_rol([2, 3]))
):
    try:
        solicitudes = cargar_datos_aprobar_solicitudes_jefeI(db, current_user)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/aprobarSolicitudes/")
def aprobar_solicitud(
    permiso: SolicitudesJefeIResponder,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_rol([2, 3]))
):
    try:
        responder_permiso(db, permiso, current_user)
        return {"message": "Solicitud aprobada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/rechazarSolicitudes/")
def rechazar_solicitud(
    permiso: SolicitudesJefeIResponder,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_rol([2, 3]))
):
    try:
        responder_permiso(db, permiso, current_user)
        return {"message": "Solicitud rechazada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))