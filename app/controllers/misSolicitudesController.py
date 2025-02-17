from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import status
from fastapi.responses import JSONResponse
from app.schemas.misSolicitudesSchema import MisSolicitudesEmpleadoCargarDatos, MisSolicitudesEmergenciaEmpleadoCargarDatos
from app.schemas.authSchema import TokenData
from datetime import datetime

def cargar_datos_ver_mis_solicitudes(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC MisSolicitudes @EmailInstitucional=:EmailInstitucional"),
            {"EmailInstitucional": current_user.email}
        )
        datos = result.mappings().all()
        
        if not datos:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[]
            )
            
        permisos = []
        for row in datos:
            try:
                # Formatear la fecha antes de crear el objeto Pydantic
                fecha_formateada = row.get("FecSolicitud").strftime('%Y-%m-%d %H:%M:%S') if row.get("FecSolicitud") else None
                
                permiso = {
                    "fec_solicitud": fecha_formateada,
                    "nom_tipo_solicitud": row.get("NomTipo", ""),
                    "nom_estado": row.get("NomEstado", ""),
                    "pri_aporbacion": row.get("PriAprobacion"),
                    "seg_aprobacion": row.get("SegAprobacion"),
                    "mot_rechazo": row.get("MotRechazo")
                }
                permisos.append(permiso)
            except Exception as row_error:
                print(f"Error procesando fila: {str(row_error)}")
                continue

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=permisos
        )
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[]
        )

def cargar_datos_ver_mis_solicitudes_emergencia(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC MisSolicitudesEmergencia @EmailInstitucional=:EmailInstitucional"),
            {"EmailInstitucional": current_user.email}
        )
        datos = result.mappings().all()
        
        if not datos:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[]
            )
            
        permisos = []
        for row in datos:
            try:
                # Formatear la fecha antes de crear el objeto Pydantic
                fecha_formateada = row.get("FecSolicitud").strftime('%Y-%m-%d %H:%M:%S') if row.get("FecSolicitud") else None
                
                permiso = {
                    "fec_solicitud": fecha_formateada,
                    "nom_tipo_solicitud": row.get("NomTipo", ""),
                    "nom_estado": row.get("NomEstado", ""),
                    "pri_aporbacion": row.get("PriAprobacion"),
                    "seg_aprobacion": row.get("SegAprobacion"),
                    "mot_rechazo": row.get("MotRechazo")
                }
                permisos.append(permiso)
            except Exception as row_error:
                print(f"Error procesando fila: {str(row_error)}")
                continue

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=permisos
        )
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[]
        )