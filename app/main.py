from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.routers import empleadoRoute, permisoPersonalRoute, authRoute
import uvicorn
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

# Configuración de CORS
origins = [
    "http://localhost:4200",
    # Agrega aquí otros orígenes permitidos si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Conexión exitosa a la base de datos"}

app.include_router(authRoute.router, prefix="/api", tags=["auth"])
app.include_router(empleadoRoute.router, prefix="/api", tags=["empleados"])
app.include_router(permisoPersonalRoute.router, prefix="/api", tags=["permisoPersonal"])

if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    uvicorn.run('app.main:app', host=host, port=port)