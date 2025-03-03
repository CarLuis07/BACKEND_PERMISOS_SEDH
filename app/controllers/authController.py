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

def change_password(db: Session, email: str, current_password: str, new_password: str):
    try:
        # Verificar la contraseña actual
        user = authenticate_user(db, email, current_password)
        if not user:
            return False
        
        # Cambiar la contraseña
        db.execute(
            text("EXEC CambiarContrasena :EmailInstitucional, :NuevaContrasena"),
            {"EmailInstitucional": email, "NuevaContrasena": new_password}
        )
        db.commit()
        return True
    except Exception as e:
        raise e