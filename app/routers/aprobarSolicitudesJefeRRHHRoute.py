from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.aprobarSolicitudesJefeRRHHSchema import SolicitudesJefeRRHHCargarDatos, SolicitudesJefeRRHHResponder
from app.schemas.authSchema import TokenData
from app.controllers.aprobarSolicitudesJefeRRHHCcontroller import cargar_datos_aprobar_solicitudes_jefeRRHH, responder_permiso
from app.routers.authRoute import get_current_active_user_with_role


router = APIRouter()

@router.get("/aprobarSolicitudesRRHH/", response_model=List[SolicitudesJefeRRHHCargarDatos])
def cargar_solicitudes(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(3))
):
    try:
        solicitudes = cargar_datos_aprobar_solicitudes_jefeRRHH(db, current_user)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/aprobarSolicitudesRRHH/")
def aprobar_solicitud(
    permiso: SolicitudesJefeRRHHResponder,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(3))
):
    try:
        responder_permiso(db, permiso, current_user)
        return {"message": "Solicitud aprobada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/rechazarSolicitudesRRHH/")
def rechazar_solicitud(
    permiso: SolicitudesJefeRRHHResponder,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(3))
):
    try:
        responder_permiso(db, permiso, current_user)
        return {"message": "Solicitud rechazada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 