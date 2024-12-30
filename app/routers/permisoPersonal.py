from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.permisoPersonalSchema import PermisosPersonalesCargarDatos
from app.controllers.permisoPersonalController import cargar_datos_para_agregar_permisos

router = APIRouter()

@router.get("/permisoPersonal/{email}", response_model=List[PermisosPersonalesCargarDatos])
def cargar_permisos(email: str, db: Session = Depends(get_db)):
    try:
        permiso = cargar_datos_para_agregar_permisos(db, email)
        if permiso:
            return permiso
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))