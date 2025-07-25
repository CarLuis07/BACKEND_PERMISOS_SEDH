from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from fastapi import HTTPException
from .schema import OfficialPermissionData, CreateOfficialPermission

class OfficialPermissionService:
    def get_employee_permissions_data(self, db: Session, email: str) -> List[OfficialPermissionData]:
        try:
            result = db.execute(
                text("EXEC CargarDatosParaAgregarPermisos :EmailInstitucional"),
                {"EmailInstitucional": email}
            )
            datos = result.mappings().all()
            permisos = []
            
            for row in datos:
                permiso = OfficialPermissionData(
                    pri_nombre=row.get("PriNombre"),
                    seg_nombre=row.get("SegNombre"),
                    pri_apellido=row.get("PriApellido"),
                    seg_apellido=row.get("SegApellido"),
                    nom_dependencia=row.get("NomDependencia"),
                    nom_cargo=row.get("NomCargo")
                )
                permisos.append(permiso)
            return permisos
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_official_permission(
        self, 
        db: Session, 
        permission: CreateOfficialPermission, 
        email: str
    ) -> None:
        try:
            db.execute(
                text("EXEC InsertarPermisoOficial :EmailInstitucional, :FecSolicitud, :Motivo"),
                {
                    "EmailInstitucional": email,
                    "FecSolicitud": permission.fecha_solicitud,
                    "Motivo": permission.motivo,
                }
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))