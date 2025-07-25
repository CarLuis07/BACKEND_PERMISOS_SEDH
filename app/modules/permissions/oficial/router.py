from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from .controller import OfficialPermissionController
from .schema import OfficialPermissionData, CreateOfficialPermission, OfficialPermissionResponse

router = APIRouter(
    prefix="/permissions/official",
    tags=["Official Permissions"]
)

permission_controller = OfficialPermissionController()

@router.get("/", response_model=List[OfficialPermissionData])
async def get_permissions_data(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtiene los datos necesarios para solicitar un permiso oficial.
    Requiere autenticación.
    """
    return await permission_controller.get_permissions_data(db, current_user)

@router.post("/", response_model=OfficialPermissionResponse)
async def create_permission(
    permission: CreateOfficialPermission,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Crea una nueva solicitud de permiso oficial.
    Requiere autenticación.
    """
    return await permission_controller.create_permission(db, permission, current_user)