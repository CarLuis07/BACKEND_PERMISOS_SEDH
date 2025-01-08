from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.misSolicitudesSchema import MisSolicitudesEmpleadoCargarDatos, MisSolicitudesEmergenciaEmpleadoCargarDatos
from app.schemas.authSchema import TokenData

def cargar_datos_ver_mis_solicitudes(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC MisSolicitudes @EmailInstitucional=:EmailInstitucional"),
            {"EmailInstitucional": current_user.email}
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            permiso = MisSolicitudesEmpleadoCargarDatos(
                fec_solicitud=row["FecSolicitud"],
                nom_tipo_solicitud=row["NomTipo"],
                nom_estado=row["NomEstado"],
                pri_aporbacion=row["PriAprobacion"],
                seg_aprobacion=row["SegAprobacion"],
                mot_rechazo=row["MotRechazo"]
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e
    
    
def cargar_datos_ver_mis_solicitudes_emergencia(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC MisSolicitudesEmergencia @EmailInstitucional=:EmailInstitucional"),
            {"EmailInstitucional": current_user.email}
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            permiso = MisSolicitudesEmergenciaEmpleadoCargarDatos(
                fec_solicitud=row["FecSolicitud"],
                nom_tipo_solicitud=row["NomTipo"],
                nom_estado=row["NomEstado"],
                pri_aporbacion=row["PriAprobacion"],
                seg_aprobacion=row["SegAprobacion"],
                mot_rechazo=row["MotRechazo"]
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e