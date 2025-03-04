from pydantic import BaseModel

class TipoContratacion(BaseModel):
    id: int
    descripcion: str

class Dependencia(BaseModel):
    id: int
    descripcion: str

class Cargo(BaseModel):
    id: int
    descripcion: str
    id_dependencia: int = None

class Sexo(BaseModel):
    id: int
    descripcion: str

class EstadoCivil(BaseModel):
    id: int
    descripcion: str

class Departamento(BaseModel):
    id: int
    descripcion: str

class Municipio(BaseModel):
    id: int
    descripcion: str
    id_departamento: int = None

class Rol(BaseModel):
    id: int
    descripcion: str

class DatosSEDH(BaseModel):
    tipos_contrataciones: list[TipoContratacion]
    dependencias: list[Dependencia]
    cargos: list[Cargo]
    sexos: list[Sexo]
    estados_civiles: list[EstadoCivil]
    departamentos: list[Departamento]
    municipios: list[Municipio]
    roles: list[Rol]