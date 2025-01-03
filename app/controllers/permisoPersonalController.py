from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.permisoPersonalSchema import PermisoPersonalEmpleadoCargarDatos, PermisoPersonalAgregarUnPermiso
from app.schemas.authSchema import TokenData


def cargar_datos_para_agregar_permisos(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarDatosParaAgregarPermisos :EmailInstitucional"),
            {"EmailInstitucional": current_user.email}
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            permiso = PermisoPersonalEmpleadoCargarDatos(
                pri_nombre=row.get("PriNombre"),
                seg_nombre=row.get("SegNombre"),
                pri_apellido=row.get("PriApellido"),
                seg_apellido=row.get("SegApellido"),
                nom_dependencia=row.get("NomDependencia"),
                nom_cargo=row.get("NomCargo")
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        raise e


def agregar_un_permiso_personal(db: Session, permiso: PermisoPersonalAgregarUnPermiso, current_user: TokenData):
    try:
        db.execute(
            text("EXEC InsertarPermisoPersonal :EmailInstitucional, :FecSolicitud, :HorSolicitadas, :Motivo, :CatEmergencia"),
            {
                "EmailInstitucional": current_user.email,
                "FecSolicitud": permiso.fecha_solicitud,
                "HorSolicitadas": permiso.horas_solicitadas,
                "Motivo": permiso.motivo,
                "CatEmergencia": permiso.catalogada_emergencia
            }
        )
        db.commit()
    except Exception as e:
        raise e