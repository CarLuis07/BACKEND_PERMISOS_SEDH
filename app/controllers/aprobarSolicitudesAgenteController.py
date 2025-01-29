from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.aprobarSolicitudesAgenteSchema import SolicitudesAgenteCargarDatos
from app.schemas.authSchema import TokenData
from datetime import time

def cargar_datos_aprobar_solicitudes_agente(db: Session, current_user: TokenData):
    try:
        result = db.execute(
            text("EXEC CargarDatosParaSolicitudesAgenteSeguridad")
        )
        datos = result.mappings().all()
        permisos = []
        for row in datos:
            horas = row.get("HorSolicitadas")
            horas_str = horas.strftime("%H:%M") if isinstance(horas, time) else None

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
                hor_solicitadas=horas_str,
            )
            permisos.append(permiso)
        return permisos
    except Exception as e:
        print(f"Error en controlador: {str(e)}")  # Debug
        raise e
