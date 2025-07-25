from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "Usuarios"
    
    id = Column(Integer, primary_key=True)
    email_institucional = Column("EmailInstitucional", String(100))
    contrasena = Column("Contrasena", String(100))
    id_rol = Column("idRol", Integer)
    activo = Column("Activo", Boolean)