from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.permisoOficialSchema import PermisoOficialEmpleadoCargarDatos, PermisoOficialAgregarUnPermiso
from app.schemas.authSchema import TokenData
from app.controllers.permisoOficialController import cargar_datos_para_agregar_permisos, agregar_un_permiso_oficial
from app.routers.authRoute import get_current_active_user


router = APIRouter()


@router.get("/permisoOficial/", response_model=List[PermisoOficialEmpleadoCargarDatos])
def cargar_permisos(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        permiso = cargar_datos_para_agregar_permisos(db, current_user)
        if permiso:
            return permiso
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/permisoOficial/")
def agregar_permiso(permiso: PermisoOficialAgregarUnPermiso, db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        agregar_un_permiso_oficial(db, permiso, current_user)
        return {"message": "Permiso agregado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    