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
        
        if not datos:
            return []
            
        permisos = []
        for row in datos:
            try:
                # Validar que existan todas las claves necesarias
                required_keys = ["NomDependencia", "Empleado", "FecSolicitud", "NomTipo"]
                for key in required_keys:
                    if key not in row:
                        print(f"Error: Falta la columna {key} en el resultado")
                        continue
                
                # Validar y convertir datos con manejo de errores
                fec_solicitud = str(row["FecSolicitud"]) if row.get("FecSolicitud") else None
                hor_salida = str(row.get("HorSalida")) if row.get("HorSalida") else None
                hor_retorno = str(row.get("HorRetorno")) if row.get("HorRetorno") else None
                hor_disponible = str(row.get("HorDisponibles")) if row.get("HorDisponibles") else None
                hor_permiso = str(row.get("HorasPermiso")) if row.get("HorasPermiso") else None

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
            except Exception as row_error:
                print(f"Error procesando fila: {str(row_error)}")
                # Continuar con la siguiente fila en caso de error
                continue
                
        return permisos
    except Exception as e:
        print(f"Error en controlador de reportePermisos: {str(e)}")
        # En lugar de propagar el error, devolver lista vacía para evitar error 500
        return []


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