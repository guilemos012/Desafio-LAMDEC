import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco (DW por padrão para a API)
DB_USER = os.getenv('DW_DB_USER', 'postgres')
DB_PASS = os.getenv('DW_DB_PASS', 'irvadigui4')
DB_HOST = os.getenv('DW_DB_HOST', 'data_warehouse')  # Nome do serviço no Docker
DB_PORT = os.getenv('DW_DB_PORT', '5432')
DB_NAME = os.getenv('DW_DB_NAME', 'LAMDEC_DW')

# String de conexão
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine
engine = create_engine(DATABASE_URL)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()