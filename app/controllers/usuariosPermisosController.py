from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.usuariosPermisoSchema import ReportePermisosEmpleadosCargarDatos
from app.schemas.authSchema import TokenData

def cargar_datos_ver_reporte_permisos_empleados(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarReportePermisosEmpleadosMes")
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            # Convertir fechas y horas a string
            fec_solicitud = row["FecSolicitud"].strftime('%Y-%m-%d') if row["FecSolicitud"] else None
            hor_salida = row["HorSalida"].strftime('%H:%M') if row["HorSalida"] else None
            hor_retorno = row["HorRetorno"].strftime('%H:%M') if row["HorRetorno"] else None
            hor_disponible = row["HorDisponibles"].strftime('%H:%M') if row["HorDisponibles"] else None
            hor_permiso = row["HorasPermiso"].strftime('%H:%M') if row["HorasPermiso"] else None

            permiso = ReportePermisosEmpleadosCargarDatos(
                nom_dependencia=row["NomDependencia"],
                empleado=row["Empleado"],
                fec_solicitud=fec_solicitud,
                nom_tipo=row["NomTipo"],
                hor_salida=hor_salida,
                hor_retorno=hor_retorno,
                hor_permiso=hor_permiso,
                hor_disponible=hor_disponible
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        raise e