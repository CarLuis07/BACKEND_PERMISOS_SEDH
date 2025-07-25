from pydantic import BaseModel
from typing import Optional

class EmployeePermissionReport(BaseModel):
    nom_dependencia: str
    empleado: str
    fec_solicitud: Optional[str]
    nom_tipo: str
    hor_salida: Optional[str]
    hor_retorno: Optional[str]
    hor_permiso: Optional[str]
    hor_disponible: Optional[str]

class EmployeeSearchResult(BaseModel):
    email_Institucional: str
    Pri_nombre: str
    Seg_nombre: str
    Pri_apellido: str
    Seg_apellido: str
    fec_Ingreso: str
    act_laboralmnete: Optional[int]
    num_identificacion: str
    num_telefono: Optional[str]
    tip_contratacion: str
    Dependencia: str
    Cargo: str
    id_jefe_inmediato: str
    sexo: str
    estado_civil: str
    municipio: Optional[str]
    departamento: Optional[str]