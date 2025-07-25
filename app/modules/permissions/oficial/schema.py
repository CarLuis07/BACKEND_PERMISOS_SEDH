from pydantic import BaseModel
from datetime import date
from typing import Optional

class OfficialPermissionBase(BaseModel):
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    nom_dependencia: str
    nom_cargo: str

class CreateOfficialPermission(BaseModel):
    fecha_solicitud: str
    motivo: str

class OfficialPermissionResponse(BaseModel):
    message: str

class OfficialPermissionData(OfficialPermissionBase):
    class Config:
        from_attributes = True