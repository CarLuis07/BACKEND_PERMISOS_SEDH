from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import time
from typing import List
from .schema import EmployeePermissionData, CreatePersonalPermission
from fastapi import HTTPException

class PersonalPermissionService:
    def get_employee_permissions_data(self, db: Session, email: str) -> List[EmployeePermissionData]:
        try:
            result = db.execute(
                text("EXEC CargarDatosParaAgregarPermisos :EmailInstitucional"),
                {"EmailInstitucional": email}
            )
            datos = result.mappings().all()
            permisos = []
            
            for row in datos:
                horas = row.get("HorDisponibles")
                horas_str = horas.strftime("%H:%M:%S") if isinstance(horas, time) else None
                
                permiso = EmployeePermissionData(
                    pri_nombre=row.get("PriNombre"),
                    seg_nombre=row.get("SegNombre"),
                    pri_apellido=row.get("PriApellido"),
                    seg_apellido=row.get("SegApellido"),
                    nom_dependencia=row.get("NomDependencia"),
                    nom_cargo=row.get("NomCargo"),
                    hor_disponibles=horas_str
                )
                permisos.append(permiso)
            return permisos
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_personal_permission(
        self, 
        db: Session, 
        permission: CreatePersonalPermission, 
        email: str
    ) -> None:
        try:
            db.execute(
                text("""EXEC InsertarPermisoPersonal 
                    :EmailInstitucional, :FecSolicitud, 
                    :HorSolicitadas, :Motivo, :CatEmergencia"""),
                {
                    "EmailInstitucional": email,
                    "FecSolicitud": permission.fecha_solicitud,
                    "HorSolicitadas": permission.horas_solicitadas,
                    "Motivo": permission.motivo,
                    "CatEmergencia": permission.citaMedica
                }
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))