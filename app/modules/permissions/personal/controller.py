from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from .service import PersonalPermissionService
from .schema import EmployeePermissionData, CreatePersonalPermission
from app.modules.auth.schema import TokenData

class PersonalPermissionController:
    def __init__(self):
        self.service = PersonalPermissionService()

    async def get_permissions_data(
        self, 
        db: Session, 
        current_user: TokenData
    ) -> List[EmployeePermissionData]:
        try:
            return self.service.get_employee_permissions_data(db, current_user.email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_permission(
        self, 
        db: Session, 
        permission: CreatePersonalPermission, 
        current_user: TokenData
    ):
        try:
            self.service.create_personal_permission(db, permission, current_user.email)
            return {"message": "Permiso agregado exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))