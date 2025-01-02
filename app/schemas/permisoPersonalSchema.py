from pydantic import BaseModel


class PermisoPersonalEmpleadoCargarDatos(BaseModel):
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    nom_dependencia: str
    nom_cargo: str

    class Config:
        orm_mode = True


class PermisoPersonalAgregarUnPermiso(BaseModel):
    fecha_solicitud: str
    horas_solicitadas: int
    motivo: str
    catalogada_emergencia: int = None

    class Config:
        orm_mode = True


class PermisoPersonalAprobacionJefeInmediato(BaseModel):
    id_permiso: int
    pri_nombre: str
    pri_apellido: str
    nom_dependencia: str
    fecha_solicitud: str
    horas_solicitadas: int
    motivo: str
    catalogada_emergencia: int = None
    motivo_rechazo: str = None

    class Config:
        orm_mode = True
