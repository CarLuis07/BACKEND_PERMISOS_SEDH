from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.aprobarSolciitudesJefeISchema import SolicitudesJefeICargarDatos, SolicitudesJefeIResponder
from app.schemas.authSchema import TokenData

def cargar_datos_aprobar_solicitudes_jefeI(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarDatosParaAprobarSolicitudesJefesI @EmailInstitucional=:EmailInstitucional"),
            {"EmailInstitucional": current_user.email}
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
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
                hor_solicitadas=row["HorSolicitadas"],
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
            text("EXEC ResponderSolicitudesJefesI :IdPermiso, :TipPermiso, :PriAprobacion, :MotRechazo"),
            {
                "IdPermiso": permiso.id_permiso,
                "TipPermiso": permiso.tip_permiso,
                "PriAprobacion": permiso.pri_aprobacion,
                "MotRechazo": permiso.mot_rechazo
            }
        )
        db.commit()
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e