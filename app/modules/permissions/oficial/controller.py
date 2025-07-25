from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from .service import OfficialPermissionService
from .schema import OfficialPermissionData, CreateOfficialPermission, OfficialPermissionResponse
from app.modules.auth.schema import TokenData

class OfficialPermissionController:
    def __init__(self):
        self.service = OfficialPermissionService()

    async def get_permissions_data(
        self, 
        db: Session, 
        current_user: TokenData
    ) -> List[OfficialPermissionData]:
        try:
            return self.service.get_employee_permissions_data(db, current_user.email)
        except Exception as e:
            raise HTTPException(
                status_code=404, 
                detail="No se encontraron datos de permisos"
            )

    async def create_permission(
        self, 
        db: Session, 
        permission: CreateOfficialPermission, 
        current_user: TokenData
    ) -> OfficialPermissionResponse:
        try:
            self.service.create_official_permission(db, permission, current_user.email)
            return {"message": "Permiso oficial agregado exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))