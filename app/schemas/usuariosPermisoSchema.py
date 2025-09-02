from pydantic import BaseModel, validator
from typing import Optional

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
    act_laboralmnete: str
    num_identificacion: str
    num_telefono: str
    tip_contratacion: str
    Dependencia: str
    Cargo: str
    id_jefe_inmediato: str
    sexo: str
    estado_civil: str
    municipio: str
    departamento: str
    
    class Config:
        orm_mode = True