# filepath: /C:/Users/kikec/Documents/python/BACKEND_PERMISOS_SEDH/app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)