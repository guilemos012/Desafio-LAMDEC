from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('DW_DB_USER')
PASSWORD = os.getenv('DW_DB_PASS')
HOST = os.getenv('DW_DB_HOST')
PORT = os.getenv('DW_DB_PORT')
DBNAME_TRANSACIONAL = os.getenv('TRANS_DB_NAME')
DBNAME_DW = os.getenv('DW_DB_NAME')

engine_transacional = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME_TRANSACIONAL}')
engine_dw = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME_DW}')