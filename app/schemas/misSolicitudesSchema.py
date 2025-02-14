from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class MisSolicitudesEmpleadoCargarDatos(BaseModel):
    fec_solicitud: datetime
    nom_tipo_solicitud: str = ""
    nom_estado: str = ""
    pri_aporbacion: Optional[str] = None
    seg_aprobacion: Optional[str] = None
    mot_rechazo: Optional[str] = None

    class Config:
        from_attributes = True


class MisSolicitudesEmergenciaEmpleadoCargarDatos(BaseModel):
    fec_solicitud: datetime
    nom_tipo_solicitud: str
    nom_estado: str
    pri_aporbacion: Optional[str] = None
    seg_aprobacion: Optional[str] = None
    mot_rechazo: Optional[str] = None

    @validator('fec_solicitud', pre=True)
    def parse_fecha(cls, value):
       
        if isinstance(value, datetime):
            return value
        try:
            # Intentar diferentes formatos de fecha
            formatos = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d'
            ]
            for formato in formatos:
                try:
                    return datetime.strptime(str(value), formato)
                except ValueError:
                    continue
            raise ValueError(f'No se pudo convertir la fecha: {value}')
        except Exception as e:
            print(f"Error al parsear fecha: {e}")
            raise ValueError(f'Error al procesar la fecha: {value}')

    class Config:
        orm_mode = True