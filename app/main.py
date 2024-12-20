from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.routers import empleado
import uvicorn
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Conexión exitosa a la base de datos"}

# Incluir las rutas definidas en la carpeta routes
app.include_router(empleado.router, prefix="/api", tags=["empleados"])

if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    uvicorn.run('app.main:app', host=host, port=port)