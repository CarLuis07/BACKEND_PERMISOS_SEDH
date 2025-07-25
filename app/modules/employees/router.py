from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from .controller import EmployeeController
from .schema import Employee
from typing import List

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

employee_controller = EmployeeController()

@router.get("/", response_model=List[Employee])
async def get_employees(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await employee_controller.get_employees(db)