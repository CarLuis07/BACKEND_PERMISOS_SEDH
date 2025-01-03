from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.permisoPersonalSchema import PermisoPersonalEmpleadoCargarDatos, PermisoPersonalAgregarUnPermiso
from app.schemas.authSchema import TokenData
from app.controllers.permisoPersonalController import cargar_datos_para_agregar_permisos, agregar_un_permiso_personal
from app.routers.authRoute import get_current_active_user


router = APIRouter()


@router.get("/permisoPersonal/", response_model=List[PermisoPersonalEmpleadoCargarDatos])
def cargar_permisos(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        permiso = cargar_datos_para_agregar_permisos(db, current_user)
        if permiso:
            return permiso
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/permisoPersonal/")
def agregar_permiso(permiso: PermisoPersonalAgregarUnPermiso, db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user)):
    try:
        agregar_un_permiso_personal(db, permiso, current_user)
        return {"message": "Permiso agregado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    