from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from .controller import PersonalPermissionController
from .schema import EmployeePermissionData, CreatePersonalPermission, PersonalPermissionResponse

router = APIRouter(
    prefix="/permissions/personal",
    tags=["Personal Permissions"]
)

permission_controller = PersonalPermissionController()

@router.get("/", response_model=List[EmployeePermissionData])
async def get_permissions_data(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtiene los datos necesarios para solicitar un permiso personal.
    """
    return await permission_controller.get_permissions_data(db, current_user)

@router.post("/", response_model=PersonalPermissionResponse)
async def create_permission(
    permission: CreatePersonalPermission,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Crea una nueva solicitud de permiso personal.
    """
    return await permission_controller.create_permission(db, permission, current_user)