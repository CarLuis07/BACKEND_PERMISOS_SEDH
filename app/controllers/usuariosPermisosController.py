from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.usuariosPermisoSchema import ReportePermisosEmpleadosCargarDatos, buscarEmpleadoPorEmail
from app.schemas.authSchema import TokenData

def cargar_datos_ver_reporte_permisos_empleados(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarReportePermisosEmpleadosMes")
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            # Validar y convertir datos
            fec_solicitud = str(row["FecSolicitud"]) if row["FecSolicitud"] else None
            hor_salida = str(row["HorSalida"]) if row["HorSalida"] else None
            hor_retorno = str(row["HorRetorno"]) if row["HorRetorno"] else None
            hor_disponible = str(row["HorDisponibles"]) if row["HorDisponibles"] else None
            hor_permiso = str(row["HorasPermiso"]) if row["HorasPermiso"] else None

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


def buscar_empleado_por_email(db: Session, email: str):
    try:
        result = db.execute(
            text("EXEC BuscarEmpleadoPorEmail @EmailInstitucional=:EmailInstitucional"),
            {"EmailInstitucional": email}
        )
        datos = result.mappings().all()
        
        if not datos:
            return None
            
        row = datos[0]  # Tomamos el primer resultado
        empleado = buscarEmpleadoPorEmail(
            email_Institucional=row["Email"],
            Pri_nombre=row["PriNombre"],
            Seg_nombre=row["SegNombre"],
            Pri_apellido=row["PriApellido"],
            Seg_apellido=row["SegApellido"],
            fec_Ingreso=str(row["FecIngreso"]),
            act_laboralmnete=row["ActLaboralmente"],
            num_identificacion=row["NumIdentificacion"],
            num_telefono=row["NumTelefono"],
            tip_contratacion=row["TipContratacion"],
            Dependencia=row["Dependencia"],
            Cargo=row["Cargo"],
            id_jefe_inmediato=row["IdJefeInmediato"],
            sexo=row["Sexo"],
            estado_civil=row["EstadoCivil"],
            municipio=row["Municipio"],
            departamento=row["Departamento"]
        )
        return empleado
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        raise e