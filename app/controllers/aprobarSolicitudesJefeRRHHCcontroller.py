from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.aprobarSolicitudesJefeRRHHSchema import SolicitudesJefeRRHHCargarDatos, SolicitudesJefeRRHHResponder
from app.schemas.authSchema import TokenData

def cargar_datos_aprobar_solicitudes_jefeRRHH(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarDatosParaAprobarSolicitudesJefeRRHH")
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            permiso = SolicitudesJefeRRHHCargarDatos(
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
                hor_solicitadas=row["HorSolicitadas"],
                cat_emergencia=row["CatEmergencia"]
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e


def responder_permiso(db: Session, permiso: SolicitudesJefeRRHHResponder, current_user: TokenData):
    try:
            
        db.execute(
            text("""EXEC ResponderSolicitudesJefeRRHH 
                @IdPermiso=:IdPermiso, 
                @TipoPermiso=:TipoPermiso, 
                @SegAprobacion=:SegAprobacion, 
                @MotRechazo=:MotRechazo,
                @HorasRechazadas=:HorasRechazadas"""),
            {
                "IdPermiso": permiso.id_permiso,
                "TipoPermiso": permiso.tipo_permiso,
                "SegAprobacion": current_user.email,
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