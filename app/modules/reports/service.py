from sqlalchemy.orm import Session
from sqlalchemy import text
from .schema import EmployeePermissionReport, EmployeeSearchResult
from typing import List, Optional

class ReportService:
    def get_employee_permissions_report(self, db: Session) -> List[EmployeePermissionReport]:
        try:
            result = db.execute(
                text("EXEC CargarReportePermisosEmpleadosMes")
            )
            datos = result.mappings().all()
            permisos = []
            
            for row in datos:
                permiso = EmployeePermissionReport(
                    nom_dependencia=row["NomDependencia"],
                    empleado=row["Empleado"],
                    fec_solicitud=str(row["FecSolicitud"]) if row["FecSolicitud"] else None,
                    nom_tipo=row["NomTipo"],
                    hor_salida=str(row["HorSalida"]) if row["HorSalida"] else None,
                    hor_retorno=str(row["HorRetorno"]) if row["HorRetorno"] else None,
                    hor_permiso=str(row["HorasPermiso"]) if row["HorasPermiso"] else None,
                    hor_disponible=str(row["HorDisponibles"]) if row["HorDisponibles"] else None
                )
                permisos.append(permiso)
            return permisos
        except Exception as e:
            print(f"Error en servicio: {str(e)}")
            raise e

    def search_employee_by_email(self, db: Session, email: str) -> Optional[EmployeeSearchResult]:
        try:
            result = db.execute(
                text("EXEC BuscarEmpleadoPorEmail @EmailInstitucional=:EmailInstitucional"),
                {"EmailInstitucional": email}
            )
            datos = result.mappings().all()
            
            if not datos:
                return None
                
            row = datos[0]
            return EmployeeSearchResult(
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
        except Exception as e:
            print(f"Error en servicio: {str(e)}")
            raise e