from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.authSchema import User

def authenticate_user(db: Session, email: str, password: str):
    try:
        result = db.execute(
            text("EXEC IngresarAlSistema :EmailInstitucional, :Contrasena"),
            {"EmailInstitucional": email, "Contrasena": password}
        )
        row = result.fetchone()
        if row:
            return User(email=row.EmailInstitucional, role=row.idRol)
        return None
    except Exception as e:
        raise e