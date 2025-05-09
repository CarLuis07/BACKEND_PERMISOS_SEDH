from pydantic import BaseModel
from typing import Optional

class EmpleadoBase(BaseModel):
    email_institucional: str
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    fech_ingreso_laboral: str 
    act_laboral: int = None
    num_identidad: str
    num_telefono: str = None
    id_tipo_contratacion: str  
    id_cargo: str  
    id_sup_inmediato: str
    id_sexo: str 
    id_estado_civil: str  
    id_municipio: str = None  


class EmpleadoCreate(BaseModel):
    email_institucional_empleado: str
    contrasena: str
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    fech_ingreso_laboral: str
    act_laboral: int = 1
    num_identidad: str
    num_telefono: str = None
    id_tipo_contratacion: int
    id_cargo: int
    id_sup_inmediato: str
    id_sexo: int
    id_estado_civil: int
    id_municipio: int
    id_rol: int

class Empleado(EmpleadoBase):
    class Config:
        orm_mode = True


class EmpleadoDetalle(BaseModel):
    email_institucional: str
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    fech_ingreso_laboral: str
    act_laboral: Optional[int] = None
    num_identidad: str
    num_telefono: Optional[str] = None
    tipo_contratacion: Optional[str] = None
    nom_dependencia: Optional[str] = None
    cargo: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    departamento: Optional[str] = None
    municipio: Optional[str] = None
    id_sup_inmediato: Optional[str] = None
    hor_disponibles: Optional[str] = None

    class Config:
        orm_mode = True

class EmpleadoEmailRequest(BaseModel):
    email_institucional: str
