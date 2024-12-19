from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.empleado import Empleado
from app.schemas.empleado import EmpleadoCreate, Empleado as EmpleadoSchema

router = APIRouter()

@router.post("/empleados/", response_model=EmpleadoSchema)
def create_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    db_empleado = Empleado(**empleado.dict())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

@router.get("/empleados/{email_institucional}", response_model=EmpleadoSchema)
def read_empleado(email_institucional: str, db: Session = Depends(get_db)):
    db_empleado = db.query(Empleado).filter(Empleado.email_institucional == email_institucional).first()
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado not found")
    return db_empleado