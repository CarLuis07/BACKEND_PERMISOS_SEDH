from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.empleadoSchema import Empleado as EmpleadoSchema
from datetime import datetime

def obtener_empleados(db: Session):
    try:
        result = db.execute(text("EXEC dbo.ObtenerEmpleados")).mappings().all()
        empleados = []
        for row in result:
            fech_ingreso_laboral = row["FecIngLaborar"]
            if isinstance(fech_ingreso_laboral, str):
                try:
                    fech_ingreso_laboral = datetime.strptime(fech_ingreso_laboral, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    fech_ingreso_laboral = datetime.strptime(fech_ingreso_laboral, '%Y-%m-%d')
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
            empleados.append(EmpleadoSchema(**empleado_data))
        return empleados
    except Exception as e:
        raise e