from fastapi import HTTPException
from sqlalchemy.orm import Session
from .service import ReportService
from .schema import EmployeePermissionReport, EmployeeSearchResult
from app.modules.auth.schema import TokenData
from typing import List, Optional

class ReportController:
    def __init__(self):
        self.report_service = ReportService()

    async def get_employee_permissions_report(
        self, 
        db: Session, 
        current_user: TokenData
    ) -> List[EmployeePermissionReport]:
        try:
            return self.report_service.get_employee_permissions_report(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_employee_by_email(
        self, 
        db: Session, 
        email: str
    ) -> Optional[EmployeeSearchResult]:
        try:
            employee = self.report_service.search_employee_by_email(db, email)
            if not employee:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró empleado con email: {email}"
                )
            return employee
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))