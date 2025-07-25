from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class Employee(Base):
    __tablename__ = "EMPLEADOS"
    
    email_institucional = Column(String, primary_key=True, index=True)
    pri_nombre = Column(String, index=True)
    seg_nombre = Column(String, index=True)
    pri_apellido = Column(String, index=True)
    seg_apellido = Column(String, index=True)
    fech_ingreso_laboral = Column(DateTime, index=True)
    act_laboral = Column(Integer, index=True)
    num_identidad = Column(String, index=True)
    num_telefono = Column(String, index=True)
    id_tipo_contratacion = Column(Integer, index=True)
    id_cargo = Column(Integer, index=True)
    id_sup_inmediato = Column(String, index=True)
    id_sexo = Column(Integer, index=True)
    id_estado_civil = Column(Integer, index=True)
    id_municipio = Column(Integer, index=True)