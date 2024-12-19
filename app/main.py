from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
import uvicorn
import os
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Conexión exitosa a la base de datos"}


if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    uvicorn.run('main:app', host=host, port=port)