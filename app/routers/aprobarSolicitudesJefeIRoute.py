from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.aprobarSolciitudesJefeISchema import SolicitudesJefeICargarDatos, SolicitudesJefeIResponder
from app.schemas.authSchema import TokenData
from app.controllers.aprobarSolicitudesJefeIController import cargar_datos_aprobar_solicitudes_jefeI, responder_permiso
from app.routers.authRoute import get_current_active_user

router = APIRouter()

@router.get("/aprobarSolicitudes/", response_model=List[SolicitudesJefeICargarDatos])
def cargar_solicitudes(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        mi_solictud = cargar_datos_aprobar_solicitudes_jefeI(db, current_user)
        if mi_solictud:
            return mi_solictud
        raise HTTPException(status_code=404, detail="Solicitudes no encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/aprobarSolicitudes/")
def aprobar_solicitud(permiso: SolicitudesJefeIResponder, db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        responder_permiso(db, permiso, current_user)
        return {"message": "Permiso aprobado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/rechazarSolicitudes/")
def rechazar_solicitud(
    permiso: SolicitudesJefeIResponder, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_active_user)
):
    try:
        responder_permiso(db, permiso, current_user)
        return {"message": "Permiso rechazado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))