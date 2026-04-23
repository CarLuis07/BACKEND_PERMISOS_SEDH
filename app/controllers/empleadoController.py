from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.empleadoSchema import Empleado as EmpleadoSchema
from app.schemas.empleadoSchema import EmpleadoDetalle
from datetime import datetime, time


def obtener_empleado_por_email(db: Session, email_institucional: str):
    try:
        query = text("EXEC dbo.BuscarEmpleadoPorEmail @EmailInstitucional=:email")
        result = db.execute(query, {"email": email_institucional}).mappings().first()
        
        if not result:
            return None
            
        fech_ingreso_laboral = result["FecIngLaborar"]
        if isinstance(fech_ingreso_laboral, str):
            try:
                fech_ingreso_laboral = datetime.strptime(fech_ingreso_laboral, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                fech_ingreso_laboral = datetime.strptime(fech_ingreso_laboral, '%Y-%m-%d')
                
        # Convertir horas disponibles a formato string "HH:MM"
        hor_disponibles = result.get("HorDisponibles")
        if isinstance(hor_disponibles, time):
            hor_disponibles = f"{hor_disponibles.hour:02d}:{hor_disponibles.minute:02d}"
        
        empleado_data = {
            "email_institucional": result["EmailInstitucional"],
            "pri_nombre": result["PriNombre"],
            "seg_nombre": result["SegNombre"],
            "pri_apellido": result["PriApellido"],
            "seg_apellido": result["SegApellido"],
            "fech_ingreso_laboral": fech_ingreso_laboral.strftime('%Y-%m-%d'),
            "act_laboral": result.get("ActLaboralmente"),
            "num_identidad": result["NumIdentidad"],
            "num_telefono": result.get("NumTelefono"),
            "tipo_contratacion": result.get("TipoContratacion"),
            "nom_dependencia": result.get("NomDependencia"),
            "cargo": result.get("Cargo"),
            "sexo": result.get("Sexo"),
            "estado_civil": result.get("EstadoCivil"),
            "departamento": result.get("Departamento"),
            "municipio": result.get("Municipio"),
            "jefe_inmediato": result.get("Jefe_Inmediato"),
            "hor_disponibles": hor_disponibles
        }
        
        return EmpleadoDetalle(**empleado_data)
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

def actualizar_empleado(db: Session, actualizador_email: str, datos: dict):
    try:
        query = text("""
            EXEC ActualizarEmpleado
            @EmailInstitucional=:email_institucional,
            @ActLaboralmente=:act_laboralmente,
            @NumTelefono=:num_telefono,
            @IdTipoContratacion=:id_tipo_contratacion,
            @IdCargo=:id_cargo,
            @NombreJefe=:nombre_jefe,
            @IdEstadoCivil=:id_estado_civil,
            @ActualizadoPor=:actualizado_por
        """)

        db.execute(query, {
            "email_institucional": datos["email_institucional"],
            "act_laboralmente": datos.get("act_laboralmente"),
            "num_telefono": datos.get("num_telefono"),
            "id_tipo_contratacion": datos.get("id_tipo_contratacion"),
            "id_cargo": datos.get("id_cargo"),
            "nombre_jefe": datos.get("nombre_jefe"),
            "id_estado_civil": datos.get("id_estado_civil"),
            "actualizado_por": actualizador_email
        })

        db.commit()
        return {"mensaje": "Empleado actualizado exitosamente"}
    except Exception as e:
        db.rollback()
        raise e