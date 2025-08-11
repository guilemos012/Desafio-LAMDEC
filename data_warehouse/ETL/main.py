from config_dw import engine_transacional, engine_dw
from extract import extract
from transform import transform
from load import load
import time
from sqlalchemy.exc import OperationalError

def wait_for_db(engine, retries=30, delay=5):
    for i in range(retries):
        try:
            # Tenta conectar
            conn = engine.connect()
            conn.close()
            print("Conexão com banco OK!")
            return True
        except OperationalError:
            print(f"Tentativa {i+1}/{retries}: banco não está pronto, aguardando {delay}s...")
            time.sleep(delay)
    print("Não foi possível conectar ao banco após várias tentativas.")
    return False

def etl():
    if not wait_for_db(engine_transacional):
        return
    if not wait_for_db(engine_dw):
        return
    dfs = extract(engine_transacional)
    dims_fato = transform(*dfs)
    load(engine_dw, *dims_fato)

if __name__ == "__main__":
    etl()