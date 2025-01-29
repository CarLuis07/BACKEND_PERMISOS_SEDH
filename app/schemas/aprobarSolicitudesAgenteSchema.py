from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class SolicitudesAgenteCargarDatos(BaseModel):
    id_permiso: int
    fec_solicitud: datetime
    nom_tipo_solicitud: str
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    nom_estado: str
    nom_dependencia: str
    nom_cargo: str
    motivo:str
    hor_solicitadas: Optional[str]

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