from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.aprobarSoliciitudesJefeISchema import SolicitudesJefeICargarDatos, SolicitudesJefeIResponder
from app.schemas.authSchema import TokenData
from datetime import time

def cargar_datos_aprobar_solicitudes_jefeI(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarDatosParaAprobarSolicitudesJefesI @EmailInstitucional=:EmailInstitucional"),
            {"EmailInstitucional": current_user.email}
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            horas = row.get("HorSolicitadas")
            horas_str = horas.strftime("%H:%M") if isinstance(horas, time) else None
        
            permiso = SolicitudesJefeICargarDatos(
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
                mot_rechazo=row["MotRechazo"],
                hor_solicitadas=horas_str,
                cat_emergencia=row["CatEmergencia"]
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e


def responder_permiso(db: Session, permiso: SolicitudesJefeIResponder, current_user: TokenData):
    try:
            
        db.execute(
            text("""EXEC ResponderSolicitudesJefesI 
                @IdPermiso=:IdPermiso, 
                @TipoPermiso=:TipoPermiso, 
                @PriAprobacion=:PriAprobacion, 
                @MotRechazo=:MotRechazo,
                @HorasRechazadas=:HorasRechazadas"""),
            {
                "IdPermiso": permiso.id_permiso,
                "TipoPermiso": permiso.tipo_permiso,
                "PriAprobacion": current_user.email,
                "MotRechazo": permiso.mot_rechazo,
                "HorasRechazadas": permiso.hor_rechazadas if permiso.mot_rechazo and permiso.tipo_permiso == 'PERMISO PERSONAL' else 0
            }
        )
        db.commit()
        return {"message": "Solicitud procesada exitosamente"}
    except Exception as e:
        print(f"Error en controlador: {str(e)}")
        db.rollback()
        raise e