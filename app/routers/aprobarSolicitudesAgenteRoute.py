from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.aprobarSolicitudesAgenteSchema import SolicitudesAgenteCargarDatos
from app.schemas.authSchema import TokenData
from app.controllers.aprobarSolicitudesAgenteController import cargar_datos_aprobar_solicitudes_agente
from app.routers.authRoute import get_current_active_user_with_role

router = APIRouter()

@router.get("/aprobarSolicitudesAgente/", response_model=List[SolicitudesAgenteCargarDatos])
def cargar_solicitudes(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(4))
):
    try:
        solicitudes = cargar_datos_aprobar_solicitudes_agente(db, current_user)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

