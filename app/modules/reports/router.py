from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from .controller import ReportController
from .schema import EmployeePermissionReport, EmployeeSearchResult

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

report_controller = ReportController()

@router.get("/permissions", response_model=List[EmployeePermissionReport])
async def get_employee_permissions_report(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtiene el reporte de permisos de empleados del mes actual.
    Requiere autenticación.
    """
    return await report_controller.get_employee_permissions_report(db, current_user)

@router.get("/employee/{email}", response_model=EmployeeSearchResult)
async def search_employee_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Busca un empleado por su correo electrónico.
    Requiere autenticación.
    """
    return await report_controller.search_employee_by_email(db, email)