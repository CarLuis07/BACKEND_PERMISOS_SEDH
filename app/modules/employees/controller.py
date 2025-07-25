from fastapi import HTTPException
from sqlalchemy.orm import Session
from .service import EmployeeService
from .schema import Employee
from typing import List

class EmployeeController:
    def __init__(self):
        self.employee_service = EmployeeService()

    async def get_employees(self, db: Session) -> List[Employee]:
        try:
            return self.employee_service.get_employees(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))