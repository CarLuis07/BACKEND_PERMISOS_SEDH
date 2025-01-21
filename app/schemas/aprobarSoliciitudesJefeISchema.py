from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class SolicitudesJefeICargarDatos(BaseModel):
    id_permiso: str
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
    mot_rechazo: Optional[str]
    hor_solicitadas: Optional[int]
    cat_emergencia: Optional[str]


    
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


class SolicitudesJefeIResponder(BaseModel):
    id_permiso: int
    tipo_permiso: str
    pri_aprobacion: Optional[str] = None
    mot_rechazo: Optional[str] = None
    hor_rechazadas: Optional[int] = None

    @validator('hor_rechazadas')
    def validar_horas_rechazo(cls, v, values):
        tipo_permiso = values.get('tipo_permiso')
        mot_rechazo = values.get('mot_rechazo')
        
        # Para PERMISO PERSONAL
        if tipo_permiso == 'PERMISO PERSONAL':
            if mot_rechazo and v is None:
                raise ValueError('Para rechazar un permiso personal se requieren las horas rechazadas')
            if not mot_rechazo and v != 0:
                raise ValueError('Si el permiso personal es aprobado, las horas rechazadas deben ser 0')
                
        # Para PERMISO OFICIAL
        if tipo_permiso == 'PERMISO OFICIAL' and v != 0:
            raise ValueError('Para permisos oficiales, las horas rechazadas deben ser 0')
            
        return v
    
    class Config:
        orm_mode = True