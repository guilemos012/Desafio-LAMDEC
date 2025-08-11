from sqlalchemy import text

def load(engine_dw, dim_pessoa, dim_natureza, dim_situacao, dim_tempo, fato_cda):
    with engine_dw.connect() as conn:
        try:
            conn.execute(text("TRUNCATE TABLE fatocda, dimpessoa, dimnaturezadivida, dimsituacaocda, dimtempo RESTART IDENTITY CASCADE"))
        except Exception as e:
            print(f"Tables don't exist yet or error truncating: {e}")
            print("Proceeding with initial load...")
    
    # Load data into tables
    dim_pessoa.to_sql('dimpessoa', engine_dw, if_exists='append', index=False)
    dim_natureza.to_sql('dimnaturezadivida', engine_dw, if_exists='append', index=False)
    dim_situacao.to_sql('dimsituacaocda', engine_dw, if_exists='append', index=False)
    dim_tempo.to_sql('dimtempo', engine_dw, if_exists='append', index=False)
    fato_cda.to_sql('fatocda', engine_dw, if_exists='append', index=False)
    
    print("ETL executado com sucesso!")