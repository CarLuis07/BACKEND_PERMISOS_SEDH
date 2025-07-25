from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from pydantic import BaseModel
from typing import Optional


class EmployeeBase(BaseModel):
    email_institucional: str
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    fech_ingreso_laboral: str 
    num_identidad: str
    id_tipo_contratacion: str  
    id_cargo: str  
    id_sup_inmediato: str
    id_sexo: str 
    id_estado_civil: str  
    act_laboral: Optional[int] = None
    num_telefono: Optional[str] = None
    id_municipio: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    pri_nombre: Optional[str] = None
    seg_nombre: Optional[str] = None
    pri_apellido: Optional[str] = None
    seg_apellido: Optional[str] = None
    act_laboral: Optional[int] = None
    num_telefono: Optional[str] = None
    id_cargo: Optional[str] = None
    id_sup_inmediato: Optional[str] = None
    id_estado_civil: Optional[str] = None
    id_municipio: Optional[str] = None

class Employee(EmployeeBase):
    class Config:
        from_attributes = True