from pydantic import BaseModel, validator
from typing import Optional, Any
from datetime import time

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


class buscarEmpleadoPorEmail(BaseModel):
    email_Institucional: str
    Pri_nombre: str
    Seg_nombre: str
    Pri_apellido: str
    Seg_apellido: str
    fec_Ingreso: str
    act_laboralmente: str  
    num_identificacion: str
    num_telefono: str
    tip_contratacion: str
    Dependencia: str
    Cargo: str
    sexo: str
    estado_civil: str
    departamento: str
    municipio: str
    id_jefe_inmediato: str
    horas_disponibles: Optional[str] = None  
    
    class Config:
        orm_mode = True