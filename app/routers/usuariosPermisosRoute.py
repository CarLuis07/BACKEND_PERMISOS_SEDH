from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.usuariosPermisoSchema import ReportePermisosEmpleadosICargarDatos
from app.schemas.authSchema import TokenData
from app.controllers.usuariosPermisosController import cargar_datos_ver_reporte_permisos_empleados
from app.routers.authRoute import get_current_active_user_with_role


router = APIRouter()


@router.get("/reportePermisos/", response_model=List[ReportePermisosEmpleadosICargarDatos])
def cargar_permisos(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user_with_role(5))):
    try:
        permiso = cargar_datos_ver_reporte_permisos_empleados(db, current_user)
        if permiso:
            return permiso
        raise HTTPException(status_code=404, detail="reportes no encontrados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))