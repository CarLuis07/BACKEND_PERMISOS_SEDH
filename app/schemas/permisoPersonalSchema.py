from pydantic import BaseModel

class PermisosPersonalesCargarDatos(BaseModel):
    pri_nombre: str
    seg_nombre: str
    pri_apellido: str
    seg_apellido: str
    nom_dependencia: str
    nom_cargo: str

    class Config:
        orm_mode = True