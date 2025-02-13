from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.usuariosPermisoSchema import ReportePermisosEmpleadosCargarDatos, buscarEmpleadoPorEmail
from app.schemas.authSchema import TokenData
from app.controllers.usuariosPermisosController import cargar_datos_ver_reporte_permisos_empleados, buscar_empleado_por_email
from app.routers.authRoute import get_current_active_user_with_role


router = APIRouter()


@router.get("/reportePermisos/", response_model=List[ReportePermisosEmpleadosCargarDatos])
def cargar_permisos(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user_with_role(5))):
    try:
        permiso = cargar_datos_ver_reporte_permisos_empleados(db, current_user)
        if permiso:
            return permiso
        raise HTTPException(status_code=404, detail="reportes no encontrados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/buscarEmpleadoPorEmail/", response_model=List[buscarEmpleadoPorEmail])
def buscar_empleado_por_email(db: Session = Depends(get_db), 
                    current_user: TokenData = Depends(get_current_active_user_with_role(5))):
    try:
        empleado = buscar_empleado_por_email(db, current_user)
        if empleado:
            return empleado
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    