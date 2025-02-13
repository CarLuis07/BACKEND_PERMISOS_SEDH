from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.usuariosPermisoSchema import buscarEmpleadoPorEmail, ReportePermisosEmpleadosCargarDatos
from app.schemas.authSchema import TokenData
from app.controllers.usuariosPermisosController import buscar_empleado_por_email, cargar_datos_ver_reporte_permisos_empleados
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
    

@router.get("/buscarEmpleadoPorEmail/{email}")
async def get_empleado_por_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user_with_role(5))
):
    try:
        empleado = buscar_empleado_por_email(db, email)
        if not empleado:
            raise HTTPException(
                status_code=404, 
                detail="Empleado no encontrado"
            )
        # Forzar respuesta JSON
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(empleado)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
