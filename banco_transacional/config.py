from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('TRANS_DB_USER')
PASSWORD = os.getenv('TRANS_DB_PASS')
HOST = os.getenv('TRANS_DB_HOST')
PORT = os.getenv('TRANS_DB_PORT')
DBNAME = os.getenv('TRANS_DB_NAME')

engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')