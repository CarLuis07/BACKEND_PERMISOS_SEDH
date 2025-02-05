from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.usuariosPermisoSchema import ReportePermisosEmpleadosICargarDatos
from app.schemas.authSchema import TokenData

def cargar_datos_ver_reporte_permisos_empleados(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarReportePermisosEmpleadosMes")
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            permiso = ReportePermisosEmpleadosICargarDatos(
                nom_dependencia=row["NomDependencia"],
                empleado=row["Empleado"],
                fec_solicitud=row["FecSolicitud"],
                nom_tipo=row["NomTipo"],
                hor_salida=row["HorSalida"],
                hor_retorno=row["HorRetorno"],
                hor_permiso=row["HorasPermiso"],
                hor_disponible=row["HorDisponibles"]
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e