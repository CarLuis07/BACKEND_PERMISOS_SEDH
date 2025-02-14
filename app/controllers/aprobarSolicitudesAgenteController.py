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
        ).mappings().all()
        
        # Mapear los resultados incluyendo el email_empleado
        permisos = []
        for row in result:
            permiso = SolicitudesAgenteCargarDatos(
                id_permiso=row['IdPermisoPersonal'],
                fec_solicitud=row['FecSolicitud'],
                nom_tipo_solicitud=row['NomTipo'],
                pri_nombre=row['PriNombre'],
                seg_nombre=row['SegNombre'],
                pri_apellido=row['PriApellido'],
                seg_apellido=row['SegApellido'],
                nom_estado=row['NomEstado'],
                nom_dependencia=row['NomDependencia'],
                nom_cargo=row['NomCargo'],
                motivo=row['Motivo'],
                hor_solicitadas=row['HorSolicitadas'].strftime('%H:%M') if row['HorSolicitadas'] else None,
                hor_salida=row['HorSalida'].strftime('%H:%M') if row['HorSalida'] else None,
                hor_retorno=row['HorRetorno'].strftime('%H:%M') if row['HorRetorno'] else None,
                email_empleado=row['EmailInstitucional']  # Agregar el correo institucional
            )
            permisos.append(permiso)
        
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
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
        # Obtener datos del procedimiento almacenado
        result = db.execute(
            text("EXEC CargarDatosParaSolicitudesAgenteSeguridad")
        ).mappings().all()
        
        solicitud_actual = next(
            (item for item in result if item['IdPermisoPersonal'] == permiso.id_permiso),
            None
        )
        
        if not solicitud_actual:
            raise ValueError(f"No se encontró la solicitud con ID {permiso.id_permiso}")

        # Convertir los valores de tiempo a formato string
        hor_solicitadas = solicitud_actual['HorSolicitadas'].strftime('%H:%M') if solicitud_actual['HorSolicitadas'] else None
        hor_salida = solicitud_actual['HorSalida'].strftime('%H:%M') if solicitud_actual['HorSalida'] else None

        # Actualizar con la hora de retorno
        db.execute(
            text("EXEC ResponderHoraRetornoAgente @IdPermiso=:IdPermiso, @TipoPermiso=:TipoPermiso, @AgenteAprobacion=:AgenteAprobacion, @HoraRetorno=:HoraRetorno"),
            {
                "IdPermiso": permiso.id_permiso,
                "TipoPermiso": permiso.tipo_permiso,
                "AgenteAprobacion": current_user.email,
                "HoraRetorno": permiso.hor_retorno
            }
        )
        db.commit()

        datos_completos = SolicitudesAgenteCargarDatos(
            id_permiso=solicitud_actual['IdPermisoPersonal'],
            fec_solicitud=solicitud_actual['FecSolicitud'],
            nom_tipo_solicitud=solicitud_actual['NomTipo'],
            pri_nombre=solicitud_actual['PriNombre'],
            seg_nombre=solicitud_actual['SegNombre'],
            pri_apellido=solicitud_actual['PriApellido'],
            seg_apellido=solicitud_actual['SegApellido'],
            nom_estado=solicitud_actual['NomEstado'],
            nom_dependencia=solicitud_actual['NomDependencia'],
            nom_cargo=solicitud_actual['NomCargo'],
            motivo=solicitud_actual['Motivo'],
            hor_solicitadas=hor_solicitadas,
            hor_salida=hor_salida,
            hor_retorno=permiso.hor_retorno,
            email_empleado=solicitud_actual['EmailInstitucional']  # Añadido el correo
        )

        email_service = EmailService()
        pdf_path = email_service.generar_pdf_permiso(datos_completos)
        # Usar el correo del empleado directamente desde datos_completos
        email_service.enviar_correo_con_pdf(datos_completos.email_empleado, pdf_path, datos_completos)

        return {"message": "Solicitud procesada y correo enviado exitosamente"}
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        db.rollback()
        raise e