from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DW_DB_USER")
PASS = os.getenv("DW_DB_PASS")
HOST = os.getenv("DW_DB_HOST")
PORT = os.getenv("DW_DB_PORT")
NAME = os.getenv("DW_DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para injetar a sessão no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()