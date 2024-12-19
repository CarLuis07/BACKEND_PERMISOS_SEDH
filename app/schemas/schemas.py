from pydantic import BaseModel
from datetime import datetime

class EmpleadoBase(BaseModel):
    email_institucional: str
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    fech_ingreso_laboral: datetime
    act_laboral: int = None
    num_identidad: str
    num_telefono: str = None
    id_tipo_contratacion: int
    id_cargo: int
    id_sup_inmediato: str
    id_sexo: int
    id_estado_civil: int
    id_municipio: int = None

class EmpleadoCreate(EmpleadoBase):
    pass

class Empleado(EmpleadoBase):
    class Config:
        orm_mode = True