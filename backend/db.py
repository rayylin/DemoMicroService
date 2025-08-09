# backend/db.py
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("SQLSERVER_USER")
PWD = os.getenv("SQLSERVER_PASSWORD")
HOST = os.getenv("SQLSERVER_HOST", "localhost")
PORT = os.getenv("SQLSERVER_PORT", "1433")
DB   = os.getenv("SQLSERVER_DB")
DRIVER = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")

# URL-encode driver
driver_enc = urllib.parse.quote_plus(DRIVER)

# Connection string (TrustServerCertificate simplifies local dev)
conn_str = (
    f"mssql+pyodbc://{USER}:{urllib.parse.quote_plus(PWD)}@{HOST}:{PORT}/"
    f"{DB}?driver={driver_enc}&TrustServerCertificate=yes"
)

engine = create_engine(conn_str, pool_pre_ping=True, fast_executemany=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)