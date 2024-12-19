from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Empleado(Base):
    __tablename__ = "EMPLEADOS"
    email_institucional = Column(String, primary_key=True, index=True, nullable=False)
    pri_nombre = Column(String, index=True, nullable=False)
    seg_nombre = Column(String, index=True, nullable=False)
    pri_apellido = Column(String, index=True, nullable=False)
    seg_apellido = Column(String, index=True, nullable=False)
    fech_ingreso_laboral = Column(DateTime, index=True, nullable=False)
    act_laboral = Column(Integer, index=True, nullable=True)
    num_identidad = Column(String, index=True, nullable=False)
    num_telefono = Column(String, index=True, nullable=True)
    id_tipo_contratacion = Column(Integer, index=True, nullable=False)
    id_cargo = Column(Integer, index=True, nullable=False)
    id_sup_inmediato = Column(String, index=True, nullable=False)
    id_sexo = Column(Integer, index=True, nullable=False)
    id_estado_civil = Column(Integer, index=True, nullable=False)
    id_municipio = Column(Integer, index=True, nullable=True)