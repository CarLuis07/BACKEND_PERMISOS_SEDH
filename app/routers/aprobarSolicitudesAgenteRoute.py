from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.aprobarSolicitudesAgenteSchema import SolicitudesAgenteCargarDatos, SolicitudesAgenteResponderHoraSalida, SolicitudesAgenteResponderHoraRetorno
from app.schemas.authSchema import TokenData
from app.controllers.aprobarSolicitudesAgenteController import cargar_datos_aprobar_solicitudes_agente, responder_agente_hora_salida, responder_agente_hora_retorno
from app.routers.authRoute import get_current_active_user_with_role

router = APIRouter()

@router.get("/aprobarSolicitudesAgenteSalida/", response_model=List[SolicitudesAgenteCargarDatos])
def cargar_solicitudes(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(4))
):
    try:
        solicitudes = cargar_datos_aprobar_solicitudes_agente(db, current_user)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/aprobarSolicitudesAgenteSalida/")
def aprobar_solicitud(
    permiso: SolicitudesAgenteResponderHoraSalida,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(4))
):
    try:
        responder_agente_hora_salida(db, permiso, current_user)
        return {"message": "Hora salida aprobada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.put("/aprobarSolicitudesAgenteRetorno/")
def aprobar_solicitud(
    permiso: SolicitudesAgenteResponderHoraRetorno,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(4))
):
    try:
        responder_agente_hora_retorno(db, permiso, current_user)
        return {"message": "Hora retorno aprobada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))