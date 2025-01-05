from sqlalchemy import Column, String, SmallInteger, Date, Time
from app.database.connection import Base

class PermisoPersonal(Base):
    __tablename__ = "PERMISOS_OFICIALES"

    id_permiso_oficial = Column(SmallInteger, primary_key=True, index=True)
    id_tipo_solicitud = Column(SmallInteger, nullable=False)
    email_institucional = Column(String(50), index=True, nullable=False)
    fecha_solicitud = Column(Date, index=True, nullable=False)
    id_estado_solicitud = Column(SmallInteger, nullable=False, default=2)
    motivo = Column(String(200), nullable=False)
    primera_aprobacion = Column(String(50), index=True)
    segunda_aprobacion = Column(String(50), index=True)
    motivo_rechazo = Column(String(100), nullable=True)
    tiempo_limite = Column(Time, nullable=True)
    hora_salida = Column(Time, nullable=True)
    hora_retorno = Column(Time, nullable=True)
    guardia_turno = Column(String(50), index=True)