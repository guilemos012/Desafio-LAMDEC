from config_dw import engine_transacional, engine_dw
from extract import extract
from transform import transform
from load import load

def etl():
    dfs = extract(engine_transacional)
    dims_fato = transform(*dfs)
    load(engine_dw, *dims_fato)

if __name__ == "__main__":
    etl()