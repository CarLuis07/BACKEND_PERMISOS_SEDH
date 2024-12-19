from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno

db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Construye la cadena de conexión
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={db_server};"
    f"DATABASE={db_name};"
    f"UID={db_user};"
    f"PWD={db_password}"
)

params = urllib.parse.quote_plus(connection_string)

# Crea el motor de conexión
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Crea una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()