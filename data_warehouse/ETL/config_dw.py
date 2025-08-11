import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Configurações do banco transacional
TRANS_DB_USER = os.getenv('TRANS_DB_USER', 'postgres')
TRANS_DB_PASS = os.getenv('TRANS_DB_PASS', 'irvadigui4')
TRANS_DB_HOST = os.getenv('TRANS_DB_HOST', 'db_transacional')  # Nome do serviço Docker
TRANS_DB_PORT = os.getenv('TRANS_DB_PORT', '5432')
TRANS_DB_NAME = os.getenv('TRANS_DB_NAME', 'LAMDEC')

# Configurações do data warehouse
DW_DB_USER = os.getenv('DW_DB_USER', 'postgres')
DW_DB_PASS = os.getenv('DW_DB_PASS', 'irvadigui4')
DW_DB_HOST = os.getenv('DW_DB_HOST', 'data_warehouse')  # Nome do serviço Docker
DW_DB_PORT = os.getenv('DW_DB_PORT', '5432')
DW_DB_NAME = os.getenv('DW_DB_NAME', 'LAMDEC_DW')

# Engines
DATABASE_URL_TRANS = f"postgresql://{TRANS_DB_USER}:{TRANS_DB_PASS}@{TRANS_DB_HOST}:{TRANS_DB_PORT}/{TRANS_DB_NAME}"
DATABASE_URL_DW = f"postgresql://{DW_DB_USER}:{DW_DB_PASS}@{DW_DB_HOST}:{DW_DB_PORT}/{DW_DB_NAME}"

engine_transacional = create_engine(DATABASE_URL_TRANS)
engine_dw = create_engine(DATABASE_URL_DW)