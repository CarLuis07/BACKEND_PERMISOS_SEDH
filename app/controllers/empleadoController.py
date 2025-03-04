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

def crear_empleado(db: Session, current_user_email: str, empleado_data: dict):
    try:
        # Construir la consulta SQL para ejecutar el procedimiento almacenado
        query = text("""
            EXEC InsertarEmpleados 
            @EmailInstitucional=:email_usuario, 
            @EmailInstitucionalEmpleado=:email_empleado, 
            @contrasena=:contrasena, 
            @PriNombre=:pri_nombre, 
            @SegNombre=:seg_nombre, 
            @PriApellido=:pri_apellido, 
            @SegApellido=:seg_apellido, 
            @FecIngLaborar=:fecha_ingreso, 
            @ActLaboralmente=:act_laboral, 
            @NumIdentidad=:num_identidad, 
            @NumTelefono=:num_telefono, 
            @IdTipoContratacion=:id_tipo_contratacion, 
            @IdCargo=:id_cargo, 
            @IdSupInmediato=:id_sup_inmediato, 
            @IdSexo=:id_sexo, 
            @IdEstadoCivil=:id_estado_civil, 
            @IdMunicipio=:id_municipio,
            @IdRol=:id_rol
        """)
        
        # Ejecutar el procedimiento almacenado
        result = db.execute(query, {
            'email_usuario': current_user_email,
            'email_empleado': empleado_data['email_institucional_empleado'],
            'contrasena': empleado_data['contrasena'],
            'pri_nombre': empleado_data['pri_nombre'],
            'seg_nombre': empleado_data['seg_nombre'],
            'pri_apellido': empleado_data['pri_apellido'],
            'seg_apellido': empleado_data['seg_apellido'],
            'fecha_ingreso': empleado_data['fech_ingreso_laboral'],
            'act_laboral': empleado_data['act_laboral'],
            'num_identidad': empleado_data['num_identidad'],
            'num_telefono': empleado_data['num_telefono'],
            'id_tipo_contratacion': empleado_data['id_tipo_contratacion'],
            'id_cargo': empleado_data['id_cargo'],
            'id_sup_inmediato': empleado_data['id_sup_inmediato'],
            'id_sexo': empleado_data['id_sexo'],
            'id_estado_civil': empleado_data['id_estado_civil'],
            'id_municipio': empleado_data['id_municipio'],
            'id_rol': empleado_data['id_rol']
        })
        
        db.commit()
        return {"mensaje": "Empleado creado exitosamente"}
    except Exception as e:
        db.rollback()
        raise e