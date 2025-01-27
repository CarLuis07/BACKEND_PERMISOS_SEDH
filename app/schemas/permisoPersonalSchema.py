from pydantic import BaseModel
from typing import Optional

class PermisoPersonalEmpleadoCargarDatos(BaseModel):
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    nom_dependencia: str
    nom_cargo: str
    hor_disponibles: Optional[str] = None

    class Config:
        orm_mode = True


class PermisoPersonalAgregarUnPermiso(BaseModel):
    fecha_solicitud: str
    horas_solicitadas: str
    motivo: str
    citaMedica: int = None

    class Config:
        orm_mode = True


class PermisoPersonalAprobacionJefeInmediato(BaseModel):
    id_permiso: int
    pri_nombre: str
    pri_apellido: str
    nom_dependencia: str
    fecha: str
    horas_solicitadas: str
    motivo: str
    citaMedica: int = None
    motivo_rechazo: str = None

    class Config:
        orm_mode = True
