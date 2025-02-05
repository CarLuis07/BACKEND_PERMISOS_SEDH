from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.routers import empleadoRoute, permisoPersonalRoute, authRoute, permisoOficialRoute, misSolicitudesRoute, aprobarSolicitudesJefeIRoute, aprobarSolicitudesJefeRRHHRoute, aprobarSolicitudesAgenteRoute
from app.auth.oauth2 import oauth2_scheme  # Import oauth2_scheme
from app.schemas import TokenData  # Import TokenData
import uvicorn
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

# Configuración de CORS
origins = [
    "http://localhost:4200",
    "http://192.168.180.26",
     "http://192.168.180.26:8000",
    # Agrega aquí otros orígenes permitidos si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ejemplo de dependencia para validar encabezados de autenticación
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Conexión exitosa a la base de datos"}

app.include_router(authRoute.router, prefix="/api", tags=["auth"])
app.include_router(empleadoRoute.router, prefix="/api", tags=["empleados"])
app.include_router(permisoPersonalRoute.router, prefix="/api", tags=["permisoPersonal"])
app.include_router(permisoOficialRoute.router, prefix="/api", tags=["permisoOficial"])
app.include_router(misSolicitudesRoute.router, prefix="/api", tags=["misSolicitudes"])
app.include_router(misSolicitudesRoute.router, prefix="/api", tags=["misSolicitudesEmergencia"])
app.include_router(aprobarSolicitudesJefeIRoute.router, prefix="/api", tags=["aprobarSolicitudes"])
app.include_router(aprobarSolicitudesJefeRRHHRoute.router, prefix="/api", tags=["aprobarSolicitudesRRHH"])
app.include_router(aprobarSolicitudesAgenteRoute.router, prefix="/api", tags=["aprobarSolicitudesAgente"])


if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    uvicorn.run('app.main:app', host=host, port=port)