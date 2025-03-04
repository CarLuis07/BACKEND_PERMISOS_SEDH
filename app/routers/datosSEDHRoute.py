from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.controllers.datosSEDHController import obtener_datos_sedh
from app.schemas.datosSEDHSchema import DatosSEDH
from app.routers.authRoute import get_current_active_user

router = APIRouter()

@router.get("/datos-sedh/", response_model=DatosSEDH)
async def read_datos_sedh(db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    try:
        return obtener_datos_sedh(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))