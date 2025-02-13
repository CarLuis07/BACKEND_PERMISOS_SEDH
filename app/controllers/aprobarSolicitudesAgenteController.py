from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.aprobarSolicitudesAgenteSchema import SolicitudesAgenteCargarDatos, SolicitudesAgenteResponderHoraSalida, SolicitudesAgenteResponderHoraRetorno
from app.schemas.authSchema import TokenData 
from datetime import time
from app.services.email_service import EmailService

def cargar_datos_aprobar_solicitudes_agente(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarDatosParaSolicitudesAgenteSeguridad")
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            horas_solicitadas = row.get("HorSolicitadas")
            horas_solicitadas_str = horas_solicitadas.strftime("%H:%M") if isinstance(horas_solicitadas, time) else None
            hora_salida = row.get("HorSalida")
            hora_salida_str = hora_salida.strftime("%H:%M") if isinstance(hora_salida, time) else None
            hora_retorno = row.get("HorRetorno")
            hora_retorno_str = hora_retorno.strftime("%H:%M") if isinstance(hora_retorno, time) else None

            permiso = SolicitudesAgenteCargarDatos(
                id_permiso=row["IdPermisoPersonal"],
                fec_solicitud=row["FecSolicitud"],
                nom_tipo_solicitud=row["NomTipo"],
                pri_nombre=row["PriNombre"],
                seg_nombre=row["SegNombre"],
                pri_apellido=row["PriApellido"],
                seg_apellido=row["SegApellido"],
                nom_estado=row["NomEstado"],
                nom_dependencia=row["NomDependencia"],
                nom_cargo=row["NomCargo"],
                motivo=row["Motivo"],
                hor_solicitadas=horas_solicitadas_str,
                hor_salida=hora_salida_str,
                hor_retorno=hora_retorno_str
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e
    

def responder_agente_hora_salida(db: Session, permiso: SolicitudesAgenteResponderHoraSalida, current_user: TokenData):
    try:
            
        db.execute(
            text("""EXEC ResponderHoraSalidaAgente 
                @IdPermiso=:IdPermiso, 
                @TipoPermiso=:TipoPermiso, 
                @AgenteAprobacion=:AgenteAprobacion, 
                @HoraSalida=:HoraSalida"""),
            {
                "IdPermiso": permiso.id_permiso,
                "TipoPermiso": permiso.tipo_permiso,
                "AgenteAprobacion": current_user.email,
                "HoraSalida": permiso.hor_salida
            }
        )
        db.commit()
        return {"message": "Solicitud procesada exitosamente"}
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        db.rollback()
        raise e
    

def responder_agente_hora_retorno(db: Session, permiso: SolicitudesAgenteResponderHoraRetorno, current_user: TokenData):
    try:
        # Obtener datos usando el procedimiento almacenado
        result = db.execute(
            text("EXEC CargarDatosParaSolicitudesAgenteSeguridad")
        ).mappings().all()
        
        # Encontrar la solicitud específica
        solicitud_actual = next(
            (item for item in result if item['id_permiso'] == permiso.id_permiso),
            None
        )
        
        if not solicitud_actual:
            raise ValueError(f"No se encontró la solicitud con ID {permiso.id_permiso}")

        # Actualizar el permiso con la hora de retorno
        db.execute(
            text("""EXEC ResponderHoraRetornoAgente 
                @IdPermiso=:IdPermiso, 
                @TipoPermiso=:TipoPermiso, 
                @AgenteAprobacion=:AgenteAprobacion, 
                @HoraRetorno=:HoraRetorno"""),
            {
                "IdPermiso": permiso.id_permiso,
                "TipoPermiso": permiso.tipo_permiso,
                "AgenteAprobacion": current_user.email,
                "HoraRetorno": permiso.hor_retorno
            }
        )
        db.commit()

        # Crear objeto con los datos del procedimiento almacenado
        datos_completos = SolicitudesAgenteCargarDatos(
            id_permiso=solicitud_actual['id_permiso'],
            fec_solicitud=solicitud_actual['fec_solicitud'],
            nom_tipo_solicitud=solicitud_actual['nom_tipo_solicitud'],
            pri_nombre=solicitud_actual['pri_nombre'],
            seg_nombre=solicitud_actual['seg_nombre'],
            pri_apellido=solicitud_actual['pri_apellido'],
            seg_apellido=solicitud_actual['seg_apellido'],
            nom_estado=solicitud_actual['nom_estado'],
            nom_dependencia=solicitud_actual['nom_dependencia'],
            nom_cargo=solicitud_actual['nom_cargo'],
            motivo=solicitud_actual['motivo'],
            hor_solicitadas=solicitud_actual['hor_solicitadas'],
            hor_salida=solicitud_actual['hor_salida'],
            hor_retorno=permiso.hor_retorno
        )

        # Generar y enviar PDF
        email_service = EmailService()
        pdf_path = email_service.generar_pdf_permiso(datos_completos)
        
        # Obtener el correo del empleado desde los datos del procedimiento
        correo_empleado = solicitud_actual['CorreoInstitucional']
        email_service.enviar_correo_con_pdf(correo_empleado, pdf_path, datos_completos)

        return {"message": "Solicitud procesada y correo enviado exitosamente"}
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        db.rollback()
        raise e