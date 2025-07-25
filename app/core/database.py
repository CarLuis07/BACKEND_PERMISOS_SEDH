from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib
from ..config.database import get_settings

settings = get_settings()

def get_connection_string():
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={settings.DB_SERVER};"
        f"DATABASE={settings.DB_NAME};"
        f"UID={settings.DB_USER};"
        f"PWD={settings.DB_PASSWORD}"
    )

def create_database_url():
    params = urllib.parse.quote_plus(get_connection_string())
    return f"mssql+pyodbc:///?odbc_connect={params}"

class Database:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()

    def init_db(self):
        if not self.engine:
            self.engine = create_engine(create_database_url())
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

    def get_db(self):
        if not self.SessionLocal:
            self.init_db()
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db = Database()
get_db = db.get_db
Base = db.Base