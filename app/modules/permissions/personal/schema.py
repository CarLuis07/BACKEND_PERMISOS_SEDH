from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class EmployeePermissionBase(BaseModel):
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    nom_dependencia: str
    nom_cargo: str
    hor_disponibles: Optional[str] = None

class CreatePersonalPermission(BaseModel):
    fecha_solicitud: date
    horas_solicitadas: str
    motivo: str
    citaMedica: bool

class PersonalPermissionResponse(BaseModel):
    message: str

class EmployeePermissionData(EmployeePermissionBase):
    class Config:
        from_attributes = True