from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.permisoPersonalSchema import PermisosPersonalesCargarDatos

def cargar_datos_para_agregar_permisos(db: Session, email_institucional: str):
    try:
        result = db.execute(
            text("EXEC CargarDatosParaAgregarPermisos :EmailInstitucional"),
            {"EmailInstitucional": email_institucional}
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            permiso = PermisosPersonalesCargarDatos(
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