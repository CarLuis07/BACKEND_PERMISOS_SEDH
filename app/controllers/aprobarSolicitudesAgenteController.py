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
# Ejecutar el procedimiento almacenado
        result = db.execute(
            text("""SELECT p.*, e.CorreoInstitucional, e.PriNombre, e.SegNombre, e.PriApellido, e.SegApellido,
                          ts.NomTipo as TipoPermiso
                   FROM PermisosPersonal p
                   JOIN Empleados e ON p.IdEmpleado = e.IdEmpleado
                   JOIN TiposSolicitud ts ON p.IdTipoSolicitud = ts.IdTipoSolicitud
                   WHERE p.IdPermisoPersonal = :IdPermiso"""),
            {"IdPermiso": permiso.id_permiso}
        ).first()
            
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
        
        # Preparar datos para el PDF
        datos_permiso = {
            "id_permiso": permiso.id_permiso,
            "fecha_solicitud": result.FecSolicitud.strftime("%Y-%m-%d"),
            "nombre_completo": f"{result.PriNombre} {result.SegNombre} {result.PriApellido} {result.SegApellido}",
            "tipo_permiso": result.TipoPermiso,
            "hora_salida": result.HorSalida.strftime("%H:%M") if result.HorSalida else "N/A",
            "hora_retorno": permiso.hor_retorno
        }

        # Enviar correo con PDF
        email_service = EmailService()
        pdf_path = email_service.generar_pdf_permiso(datos_permiso)
        email_service.enviar_correo_con_pdf(result.CorreoInstitucional, pdf_path, datos_permiso)

        return {"message": "Solicitud procesada y correo enviado exitosamente"}
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        db.rollback()
        raise e