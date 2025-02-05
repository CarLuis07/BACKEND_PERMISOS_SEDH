from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class ReportePermisosEmpleadosCargarDatos(BaseModel):
    nom_dependencia: str
    empleado: str
    fec_solicitud: str
    nom_tipo: str
    hor_salida: Optional[str]
    hor_retorno: Optional[str]
    hor_permiso: Optional[str]
    hor_disponible: Optional[str]

    class Config:
        orm_mode = True