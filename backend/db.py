# backend/db.py
import os, urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DRIVER = os.getenv("SQLSERVER_DRIVER")
SERVER = os.getenv("SQLSERVER_SERVER")
DATABASE = os.getenv("SQLSERVER_DB")
TRUSTED_CONNECTION = os.getenv("SQLSERVER_TRUSTED_CONNECTION", "yes")
TRUST_SERVER_CERTIFICATE = os.getenv("SQLSERVER_TRUST_SERVER_CERTIFICATE", "yes")
MARS = os.getenv("SQLSERVER_MARS", "True")

odbc_str = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection={TRUSTED_CONNECTION};"
    f"TrustServerCertificate={TRUST_SERVER_CERTIFICATE};"
    f"MultipleActiveResultSets={MARS};"
)

connect_url = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(odbc_str)

engine = create_engine(connect_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)