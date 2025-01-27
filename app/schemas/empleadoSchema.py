from pydantic import BaseModel

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

class EmpleadoCreate(EmpleadoBase):
    pass

class Empleado(EmpleadoBase):
    class Config:
        orm_mode = True

