from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.aprobarSolciitudesJefeISchema import AprobarSolicitudesJefeICargarDatos
from app.schemas.authSchema import TokenData
from app.controllers.aprobarSolicitudesJefeIController import cargar_datos_aprobar_solicitudes_jefeI
from app.routers.authRoute import get_current_active_user

router = APIRouter()

@router.get("/aprobarSolicitudes/", response_model=List[AprobarSolicitudesJefeICargarDatos])
def cargar_mis_solcitudes(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        mi_solictud = cargar_datos_aprobar_solicitudes_jefeI(db, current_user)
        if mi_solictud:
            return mi_solictud
        raise HTTPException(status_code=404, detail="Solicitudes no encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))