from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from .schema import Employee, EmployeeCreate, EmployeeUpdate
from typing import List

class EmployeeService:
    def get_employees(self, db: Session) -> List[Employee]:
        try:
            result = db.execute(text("EXEC dbo.ObtenerEmpleados")).mappings().all()
            empleados = []
            for row in result:
                fech_ingreso_laboral = self._parse_date(row["FecIngLaborar"])
                empleado_data = {
                    "email_institucional": row["EmailInstitucional"],
                    "pri_nombre": row["PriNombre"],
                    "seg_nombre": row["SegNombre"],
                    "pri_apellido": row["PriApellido"],
                    "seg_apellido": row["SegApellido"],
                    "fech_ingreso_laboral": fech_ingreso_laboral.strftime('%Y-%m-%d'),
                    "act_laboral": row.get("ActLaboralmente"),
                    "num_identidad": row["NumIdentidad"],
                    "num_telefono": row.get("NumTelefono"),
                    "id_tipo_contratacion": row["TipoContratacion"],
                    "id_cargo": row["Cargo"],
                    "id_sup_inmediato": row["IdSupInmediato"],
                    "id_sexo": row["Sexo"],
                    "id_estado_civil": row["EstadoCivil"],
                    "id_municipio": row.get("Municipio")
                }
                empleados.append(Employee(**empleado_data))
            return empleados
        except Exception as e:
            raise e

    def _parse_date(self, date_str: str) -> datetime:
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return datetime.strptime(date_str, '%Y-%m-%d')
        return date_str